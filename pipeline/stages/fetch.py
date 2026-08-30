"""
fetch.py — Stage 1
Read every non-header row from the configured Google Sheet.
Returns a list of raw dicts keyed by column header.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import gspread
from google.oauth2.service_account import Credentials


_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def _get_credentials() -> Credentials:
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    # Accept either a file path or inline JSON blob
    if raw.strip().startswith("{"):
        info = json.loads(raw)
    else:
        info = json.loads(Path(raw).read_text(encoding="utf-8"))
    return Credentials.from_service_account_info(info, scopes=_SCOPES)


def fetch_rows() -> list[dict[str, Any]]:
    """Return all data rows from the Google Sheet as a list of dicts."""
    creds = _get_credentials()
    client = gspread.authorize(creds)

    sheet_id = os.environ["GOOGLE_SHEET_ID"]
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.get_worksheet(0)  # first sheet tab

    records = worksheet.get_all_records(
        default_blank=None,
        value_render_option="UNFORMATTED_VALUE",
    )
    return list(records)
