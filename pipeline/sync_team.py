#!/usr/bin/env python3
"""
sync_team.py — Entry point for the Google Sheet -> Django team pipeline.

Usage:
    cd pipeline
    pip install -r requirements.txt
    cp .env.example .env        # then fill in credentials
    python sync_team.py

The pipeline is idempotent: running it multiple times with the same sheet
data will not create duplicate team members (deduplication is by email).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Allow running from the project root or from the pipeline/ directory
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load .env from the pipeline directory
load_dotenv(Path(__file__).parent / ".env")

from stages.fetch import fetch_rows
from stages.clean import clean_rows
from stages.validate import validate_rows
from stages.transform import transform_rows
from stages.sync import sync_members

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("━━━ STAGE 1: fetch ━━━━━━━━━━━━━━━━━━━━━━━━━")
    raw_rows = fetch_rows()
    logger.info("Fetched %d rows from Google Sheet.", len(raw_rows))

    if not raw_rows:
        logger.warning("Sheet is empty — nothing to sync.")
        return 0

    logger.info("━━━ STAGE 2: clean ━━━━━━━━━━━━━━━━━━━━━━━━━")
    cleaned = clean_rows(raw_rows)
    logger.info("Cleaned %d rows.", len(cleaned))

    logger.info("━━━ STAGE 3: validate ━━━━━━━━━━━━━━━━━━━━━━━")
    valid, rejected = validate_rows(cleaned)
    logger.info("Valid: %d  |  Rejected: %d", len(valid), len(rejected))
    for row in rejected:
        logger.warning(
            "  REJECTED %r — %s",
            row.get("Name") or row.get("Timestamp") or "?",
            row["_reject_reason"],
        )

    if not valid:
        logger.warning("No valid rows after validation — nothing to sync.")
        return 0

    logger.info("━━━ STAGE 4: transform ━━━━━━━━━━━━━━━━━━━━━━")
    payloads = transform_rows(valid)
    logger.info("Transformed %d payloads.", len(payloads))

    logger.info("━━━ STAGE 5: sync ━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    result = sync_members(payloads)

    logger.info("━━━ RESULT ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    logger.info(
        "Created: %d  |  Updated: %d  |  Failed: %d",
        result.created, result.updated, result.failed,
    )

    if result.errors:
        logger.warning("Errors:")
        for err in result.errors:
            logger.warning("  %s — %s", err["name"], err["error"])

    return 1 if result.failed else 0


if __name__ == "__main__":
    sys.exit(main())
