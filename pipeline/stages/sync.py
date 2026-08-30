"""
sync.py — Stage 5
Authenticate with Django via the JWT token endpoint, then upsert
each transformed member payload via the new /server/team/member/ endpoint.

Authentication flow:
  POST /mentor/token/  {username, password}  ->  {access, refresh}
  Use `access` token as Bearer in subsequent requests.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Any

import requests

logger = logging.getLogger(__name__)

# ─── Config ───────────────────────────────────────────────────────────────────

_BASE_URL = os.environ.get("DJANGO_API_URL", "https://codeutsava.nitrr.ac.in").rstrip("/")
_TOKEN_ENDPOINT = f"{_BASE_URL}/mentor/token/"
_MEMBER_ENDPOINT = f"{_BASE_URL}/server/team/member/"

_RETRY_ATTEMPTS = 3
_RETRY_DELAY = 2  # seconds between retries


# ─── Result types ─────────────────────────────────────────────────────────────


@dataclass
class SyncResult:
    created: int = 0
    updated: int = 0
    failed: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)


# ─── Auth ─────────────────────────────────────────────────────────────────────


def _get_access_token() -> str:
    """Obtain a JWT access token using admin credentials from environment."""
    username = os.environ["DJANGO_ADMIN_USER"]
    password = os.environ["DJANGO_ADMIN_PASS"]

    res = requests.post(
        _TOKEN_ENDPOINT,
        json={"username": username, "password": password},
        timeout=15,
    )
    res.raise_for_status()
    token: str = res.json()["access"]
    return token


# ─── Upsert ───────────────────────────────────────────────────────────────────


def _upsert(payload: dict[str, object], token: str) -> dict[str, Any]:
    """POST the payload to the upsert endpoint. Raises on HTTP error."""
    for attempt in range(1, _RETRY_ATTEMPTS + 1):
        try:
            res = requests.post(
                _MEMBER_ENDPOINT,
                json=payload,
                headers={"Authorization": f"Bearer {token}"},
                timeout=20,
            )
            if res.status_code == 401:
                # Token may have expired; bubble up so caller can refresh
                raise requests.HTTPError("401 Unauthorized", response=res)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as exc:
            if attempt == _RETRY_ATTEMPTS:
                raise
            logger.warning("Attempt %d/%d failed: %s. Retrying…", attempt, _RETRY_ATTEMPTS, exc)
            time.sleep(_RETRY_DELAY * attempt)

    # Unreachable but satisfies type checkers
    raise RuntimeError("Unreachable")


# ─── Public API ───────────────────────────────────────────────────────────────


def sync_members(payloads: list[dict[str, object]]) -> SyncResult:
    """
    Upsert all payloads into the Django backend.
    Authenticates once at the start; re-authenticates on 401.
    """
    if not payloads:
        logger.info("No payloads to sync.")
        return SyncResult()

    result = SyncResult()
    token = _get_access_token()

    for i, payload in enumerate(payloads, start=1):
        name = payload.get("name", f"row {i}")
        try:
            response = _upsert(payload, token)
            if response.get("created"):
                result.created += 1
                logger.info("[%d/%d] CREATED  %s", i, len(payloads), name)
            else:
                result.updated += 1
                logger.info("[%d/%d] UPDATED  %s", i, len(payloads), name)
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 401:
                # Refresh token and retry this payload once
                logger.warning("Token expired; re-authenticating…")
                try:
                    token = _get_access_token()
                    response = _upsert(payload, token)
                    if response.get("created"):
                        result.created += 1
                    else:
                        result.updated += 1
                    continue
                except Exception as retry_exc:
                    logger.error("[%d/%d] FAILED (after re-auth) %s: %s", i, len(payloads), name, retry_exc)
            else:
                logger.error(
                    "[%d/%d] FAILED %s: HTTP %s — %s",
                    i, len(payloads), name,
                    exc.response.status_code if exc.response is not None else "?",
                    exc.response.text[:200] if exc.response is not None else str(exc),
                )
            result.failed += 1
            result.errors.append({"name": name, "error": str(exc)})
        except Exception as exc:
            logger.error("[%d/%d] FAILED %s: %s", i, len(payloads), name, exc)
            result.failed += 1
            result.errors.append({"name": name, "error": str(exc)})

    return result
