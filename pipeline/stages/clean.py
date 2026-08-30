"""
clean.py — Stage 2
Strip, normalise and lightly sanitise raw Google Sheet rows.
Each rule is field-specific; we do NOT destroy valid content.
"""

from __future__ import annotations

import html
import re
from typing import Any

# ─── Field-level cleaners ─────────────────────────────────────────────────────


def _clean_str(value: Any) -> str:
    """Convert to string, strip leading/trailing whitespace, collapse internal runs."""
    if value is None:
        return ""
    text = str(value).strip()
    # Collapse multiple internal whitespace characters to a single space
    text = re.sub(r"\s+", " ", text)
    return text


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode entities (XSS prevention)."""
    # Decode HTML entities first so &lt;script&gt; becomes <script> before stripping
    text = html.unescape(text)
    # Strip tags
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def _clean_name(value: Any) -> str:
    text = _clean_str(value)
    text = _strip_html(text)
    # Allow letters (including Unicode), spaces, hyphens, apostrophes, dots
    # Remove anything else
    text = re.sub(r"[^\w\s\-\'.]+", "", text, flags=re.UNICODE)
    return text[:100]  # model max_length


def _clean_email(value: Any) -> str:
    text = _clean_str(value).lower()
    return text[:254]


def _clean_url(value: Any) -> str:
    """Strip whitespace; do NOT modify the URL content."""
    return _clean_str(value)


def _clean_role(value: Any) -> str:
    """Normalise role: strip, collapse whitespace, title-case."""
    text = _clean_str(value)
    text = _strip_html(text)
    # Normalise to title case so 'overall coordinator' == 'Overall Coordinator'
    return text.title()


def _clean_domain(value: Any) -> str:
    text = _clean_str(value)
    text = _strip_html(text)
    return text


def _clean_branch(value: Any) -> str:
    return _clean_str(value).upper()


# ─── Row cleaner ─────────────────────────────────────────────────────────────


# Map Google Sheet column headers → cleaner function
_FIELD_CLEANERS: dict[str, Any] = {
    "Name": _clean_name,
    "Photo": _clean_url,
    "Designation in TCP": _clean_role,
    "Domain": _clean_domain,
    "Branch": _clean_branch,
    "Year": lambda v: _clean_str(v),
    "LinkedIn": _clean_url,
    "Instagram": _clean_url,
    "GitHub": _clean_url,
    "Timestamp": _clean_str,
}


def clean_row(raw: dict[str, Any]) -> dict[str, str]:
    """Apply field-specific cleaning to a single raw sheet row."""
    cleaned: dict[str, str] = {}
    for col, cleaner in _FIELD_CLEANERS.items():
        cleaned[col] = cleaner(raw.get(col))
    return cleaned


def clean_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [clean_row(row) for row in rows]
