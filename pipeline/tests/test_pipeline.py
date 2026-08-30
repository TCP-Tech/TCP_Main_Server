"""
tests/test_pipeline.py
Unit tests covering all scenarios from the spec.
Run with:  python -m unittest discover -s tests
"""

import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

# Allow imports from the pipeline/ directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from stages.clean import clean_row, clean_rows
from stages.validate import validate_rows
from stages.transform import transform_row


def _make_row(**overrides) -> dict:
    """Return a minimal valid cleaned row with optional overrides."""
    base = {
        "Name": "Test Member",
        "Photo": "https://drive.google.com/file/d/abc123/view",
        "Designation in TCP": "Manager",
        "Domain": "Technical",
        "Branch": "CSE",
        "Year": "2026",
        "LinkedIn": "https://linkedin.com/in/test",
        "Instagram": "",
        "GitHub": "",
        "Timestamp": "2026-08-01 10:00:00",
    }
    base.update(overrides)
    return base


class PipelineTests(TestCase):
    def test_valid_member(self):
        row = _make_row()
        valid, rejected = validate_rows([row])
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 0)
        payload = transform_row(valid[0])
        self.assertEqual(payload["name"], "Test Member")
        self.assertEqual(payload["member_type"], "MNG")

    def test_missing_name(self):
        row = _make_row(Name="")
        _, rejected = validate_rows([row])
        self.assertEqual(len(rejected), 1)
        self.assertIn("name", rejected[0]["_reject_reason"].lower())

    def test_extra_whitespace_cleaned(self):
        raw = {
            "Name": "  Alice   Bob  ",
            "Designation in TCP": " Manager  ",
            "Domain": "  Technical  ",
            "Branch": " CSE ",
            "Year": "2026",
            "LinkedIn": "",
            "Instagram": "",
            "GitHub": "",
            "Photo": "",
            "Timestamp": "",
        }
        cleaned = clean_row(raw)
        self.assertEqual(cleaned["Name"], "Alice Bob")
        self.assertEqual(cleaned["Designation in TCP"], "Manager")
        self.assertEqual(cleaned["Domain"], "Technical")
        self.assertEqual(cleaned["Branch"], "CSE")

    def test_invalid_role_rejected(self):
        row = _make_row(**{"Designation in TCP": "Volunteer"})
        _, rejected = validate_rows([row])
        self.assertEqual(len(rejected), 1)

    def test_duplicate_member_is_update(self):
        from stages.sync import sync_members

        payload = {"name": "Alice", "email": "alice@test.com", "member_type": "MNG", "year": 2026}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"created": False, "message": "Member updated.", "data": payload}
        mock_response.raise_for_status = MagicMock()

        with patch("stages.sync._get_access_token", return_value="fake-token"), \
             patch("stages.sync.requests.post", return_value=mock_response):
            result = sync_members([payload])

        self.assertEqual(result.created, 0)
        self.assertEqual(result.updated, 1)
        self.assertEqual(result.failed, 0)

    def test_invalid_linkedin_url(self):
        row = _make_row(LinkedIn="not-a-url")
        _, rejected = validate_rows([row])
        self.assertEqual(len(rejected), 1)
        self.assertIn("linkedin", rejected[0]["_reject_reason"].lower())

    def test_html_script_stripped_from_name(self):
        raw = {
            "Name": '<script>alert("xss")</script>Alice',
            "Designation in TCP": "Manager",
            "Domain": "Technical",
            "Branch": "CSE",
            "Year": "2026",
            "LinkedIn": "",
            "Instagram": "",
            "GitHub": "",
            "Photo": "",
            "Timestamp": "",
        }
        cleaned = clean_row(raw)
        self.assertNotIn("<script>", cleaned["Name"])
        self.assertIn("Alice", cleaned["Name"])

    def test_javascript_url_rejected(self):
        row = _make_row(LinkedIn="javascript:alert(1)")
        _, rejected = validate_rows([row])
        self.assertEqual(len(rejected), 1)

    def test_multiple_roles_in_single_field_rejected(self):
        row = _make_row(**{"Designation in TCP": "Manager, Executive"})
        _, rejected = validate_rows([row])
        self.assertEqual(len(rejected), 1)

    def test_empty_sheet(self):
        valid, rejected = validate_rows([])
        self.assertEqual(valid, [])
        self.assertEqual(rejected, [])

    def test_api_failure_counted(self):
        import requests as req
        from stages.sync import sync_members

        payload = {"name": "Bob", "member_type": "EXC", "year": 2026}

        with patch("stages.sync._get_access_token", return_value="fake-token"), \
             patch("stages.sync.requests.post", side_effect=req.ConnectionError("down")):
            result = sync_members([payload])

        self.assertEqual(result.failed, 1)
        self.assertEqual(result.created, 0)

    def test_missing_image_gives_null(self):
        row = _make_row(Photo="")
        payload = transform_row(row)
        self.assertIsNone(payload["drive_image_url"])

    def test_pipeline_idempotent(self):
        from stages.sync import sync_members

        payload = {"name": "Carol", "email": "carol@test.com", "member_type": "HCO", "year": 2026}

        mock_created = MagicMock()
        mock_created.status_code = 201
        mock_created.json.return_value = {"created": True, "message": "Member created.", "data": payload}
        mock_created.raise_for_status = MagicMock()

        mock_updated = MagicMock()
        mock_updated.status_code = 200
        mock_updated.json.return_value = {"created": False, "message": "Member updated.", "data": payload}
        mock_updated.raise_for_status = MagicMock()

        with patch("stages.sync._get_access_token", return_value="fake-token"), \
             patch("stages.sync.requests.post", return_value=mock_created):
            r1 = sync_members([payload])

        with patch("stages.sync._get_access_token", return_value="fake-token"), \
             patch("stages.sync.requests.post", return_value=mock_updated):
            r2 = sync_members([payload])

        self.assertEqual(r1.created, 1)
        self.assertEqual(r1.failed, 0)
        self.assertEqual(r2.updated, 1)
        self.assertEqual(r2.failed, 0)
