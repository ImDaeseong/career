"""Regression tests for evidence and application validation."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from career_tracker import summarize_tracker, validate_tracker  # noqa: E402


class CareerTrackerTests(unittest.TestCase):
    """Protect evidence provenance and outcome aggregation rules."""

    def setUp(self) -> None:
        self.data = json.loads((ROOT / "examples/career-tracker.example.json").read_text(encoding="utf-8"))

    def test_example_is_valid_and_report_is_observational(self) -> None:
        self.assertEqual(validate_tracker(self.data), [])
        self.assertEqual(
            summarize_tracker(self.data),
            {"applications": 1, "stages": {"applied": 1}, "requirements": {"covered": 1, "gap": 1}},
        )

    def test_covered_requirement_requires_evidence_for_that_failure_reason(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["applications"][0]["requirements"][0]["evidence_ids"] = []
        self.assertEqual(
            validate_tracker(invalid),
            ["applications[0].requirements[0] covered requires evidence"],
        )

    def test_unknown_evidence_reports_the_unknown_identifier(self) -> None:
        invalid = copy.deepcopy(self.data)
        invalid["applications"][0]["requirements"][0]["evidence_ids"] = ["missing"]
        self.assertEqual(
            validate_tracker(invalid),
            ["applications[0].requirements[0] unknown evidence: missing"],
        )


if __name__ == "__main__":
    unittest.main()
