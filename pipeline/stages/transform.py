"""
transform.py — Stage 4
Map validated Google Sheet rows into Django API payloads.

Google Sheet columns:
  Timestamp | Name | Photo | Designation in TCP | Domain | Branch | Year | LinkedIn | Instagram | GitHub

Django model fields:
  name | branch | image | member_type | year | domain | linkedin | instagram | github | email | drive_image_url
"""

from __future__ import annotations

import os
import re
from urllib.parse import urlparse

from .validate import ROLE_ALLOWLIST


# ─── Drive URL normaliser ─────────────────────────────────────────────────────


def _normalise_drive_url(url: str) -> str:
    """Convert a Google Drive share URL to a direct-download URL."""
    if not url:
        return url
    try:
        parsed = urlparse(url)
    except ValueError:
        return url
    if "drive.google.com" not in parsed.netloc:
        return url

    # /file/d/{id}/...
    match = re.search(r"/file/d/([^/?]+)", parsed.path)
    if match:
        return f"https://drive.google.com/uc?export=view&id={match.group(1)}"

    # ?id=...
    id_param = parsed.query and next(
        (v for k, v in (p.split("=", 1) for p in parsed.query.split("&") if "=" in p) if k == "id"),
        None,
    )
    if id_param:
        return f"https://drive.google.com/uc?export=view&id={id_param}"

    return url


# ─── Domain normaliser ────────────────────────────────────────────────────────


def _normalise_domain(domain: str) -> str:
    """Ensure domain matches the Django model choices exactly."""
    mapping = {
        "Sponsorship": "sponsorship",
        "Pr & Marketing": "PR & Marketing",
        "PR & Marketing": "PR & Marketing",
        "Technical": "Technical",
        "Documentation": "Documentation",
        "Design": "Design",
        "Video Editing": "Video Editing",
    }
    return mapping.get(domain, domain)


# ─── Row transformer ──────────────────────────────────────────────────────────


def transform_row(row: dict[str, str]) -> dict[str, object]:
    """Map a single validated sheet row to a Django API payload dict."""
    year = int(row.get("Year") or os.environ.get("TEAM_YEAR", "2026"))

    return {
        "name": row["Name"],
        "branch": row.get("Branch") or "CSE",
        "member_type": ROLE_ALLOWLIST[row["Designation in TCP"]],
        "year": year,
        "domain": _normalise_domain(row.get("Domain", "")),
        "linkedin": row.get("LinkedIn") or None,
        "instagram": row.get("Instagram") or None,
        "github": row.get("GitHub") or None,
        "email": row.get("Email") or None,
        "drive_image_url": _normalise_drive_url(row.get("Photo", "")) or None,
        # `image` field is left as-is (file upload not supported by pipeline)
    }


def transform_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    return [transform_row(row) for row in rows]
