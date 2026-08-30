"""
validate.py — Stage 3
Validate cleaned rows against business rules.
Returns (valid_rows, rejected_rows).
Rejected rows include a human-readable `_reject_reason` key.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

# ─── Allowlists ───────────────────────────────────────────────────────────────

# Map cleaned sheet values -> Django member_type code
ROLE_ALLOWLIST: dict[str, str] = {
    "Overall Coordinator": "OCO",
    "Head Coordinator": "HCO",
    "Manager": "MNG",
    "Executive": "EXC",
}

BRANCH_ALLOWLIST = {
    "CSE", "IT", "ECE", "ELEC", "MECH", "CHEM",
    "CIVIL", "META", "MIN", "BIOMED", "BIOTECH", "MCA",
}

DOMAIN_ALLOWLIST = {
    "Technical",
    "Sponsorship",
    "PR & Marketing",
    "Documentation",
    "Design",
    "Video Editing",
}

# ─── Validators ───────────────────────────────────────────────────────────────

_EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
)


def _is_valid_url(url: str) -> bool:
    """Return True for http(s) URLs; rejects javascript: and empty strings."""
    if not url:
        return True  # empty URL is acceptable (field is optional)
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc:
        return False
    return True


def _validate_row(row: dict[str, str]) -> str | None:
    """Return a reject reason string, or None if the row is valid."""

    # Required: Name
    if not row.get("Name"):
        return "Missing name"

    # Required: Designation in TCP (role)
    role = row.get("Designation in TCP", "")
    if role not in ROLE_ALLOWLIST:
        return f"Unknown role: {role!r}. Allowed: {list(ROLE_ALLOWLIST)}"

    # Branch (optional but must be from allowlist if provided)
    branch = row.get("Branch", "")
    if branch and branch not in BRANCH_ALLOWLIST:
        return f"Unknown branch: {branch!r}"

    # Domain: required for non-overall-coordinator roles
    domain = row.get("Domain", "")
    if ROLE_ALLOWLIST[role] != "OCO":
        # Normalise sponsorship -> Sponsorship
        domain_norm = domain.strip().title().replace("Pr &", "PR &")
        if domain_norm not in DOMAIN_ALLOWLIST:
            return f"Unknown domain: {domain!r}. Allowed: {list(DOMAIN_ALLOWLIST)}"

    # Email: optional but must be valid if provided
    email = row.get("Email", "")
    if email and not _EMAIL_RE.match(email):
        return f"Invalid email: {email!r}"

    # URL fields
    for field in ("LinkedIn", "Instagram", "GitHub", "Photo"):
        url = row.get(field, "")
        if not _is_valid_url(url):
            return f"Invalid URL in {field}: {url!r}"

    return None  # valid


def validate_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """
    Returns:
        (valid_rows, rejected_rows)
    Each rejected row has an extra `_reject_reason` key.
    """
    valid: list[dict[str, str]] = []
    rejected: list[dict[str, Any]] = []

    for row in rows:
        reason = _validate_row(row)
        if reason is None:
            valid.append(row)
        else:
            rejected.append({**row, "_reject_reason": reason})

    return valid, rejected
