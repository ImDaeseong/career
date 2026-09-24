"""Validate evidence-backed applications and summarize observed job-search outcomes."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


STAGES = {"applied", "screen", "interview", "offer", "rejected", "withdrawn"}
COVERAGE = {"covered", "partial", "gap"}


def load_tracker(path: Path) -> dict:
    """Load one tracker document from UTF-8 JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def validate_tracker(data: dict) -> list[str]:
    """Return stable diagnostics for invalid evidence and application links."""
    errors: list[str] = []
    evidence = data.get("evidence", [])
    applications = data.get("applications", [])
    evidence_ids = [item.get("id") for item in evidence]
    duplicate_ids = sorted({item for item in evidence_ids if item and evidence_ids.count(item) > 1})
    if duplicate_ids:
        errors.append(f"duplicate evidence id: {', '.join(duplicate_ids)}")
    known_evidence = {item for item in evidence_ids if item}

    for index, item in enumerate(evidence):
        for field in ("id", "claim", "source", "verified_at"):
            if not item.get(field):
                errors.append(f"evidence[{index}] missing {field}")
        if not isinstance(item.get("public"), bool):
            errors.append(f"evidence[{index}] public must be boolean")

    application_ids: set[str] = set()
    for index, application in enumerate(applications):
        prefix = f"applications[{index}]"
        app_id = application.get("id")
        if not app_id:
            errors.append(f"{prefix} missing id")
        elif app_id in application_ids:
            errors.append(f"duplicate application id: {app_id}")
        else:
            application_ids.add(app_id)
        if application.get("stage") not in STAGES:
            errors.append(f"{prefix} invalid stage: {application.get('stage')}")
        for req_index, requirement in enumerate(application.get("requirements", [])):
            req_prefix = f"{prefix}.requirements[{req_index}]"
            status = requirement.get("status")
            linked = requirement.get("evidence_ids", [])
            if status not in COVERAGE:
                errors.append(f"{req_prefix} invalid status: {status}")
            missing = sorted(set(linked) - known_evidence)
            if missing:
                errors.append(f"{req_prefix} unknown evidence: {', '.join(missing)}")
            if status == "covered" and not linked:
                errors.append(f"{req_prefix} covered requires evidence")
    return errors


def summarize_tracker(data: dict) -> dict:
    """Count recorded stages and requirement coverage without causal claims."""
    applications = data.get("applications", [])
    stages = Counter(item["stage"] for item in applications)
    coverage = Counter(
        requirement["status"]
        for application in applications
        for requirement in application.get("requirements", [])
    )
    return {
        "applications": len(applications),
        "stages": dict(sorted(stages.items())),
        "requirements": dict(sorted(coverage.items())),
    }


def main(argv: list[str] | None = None) -> int:
    """Run validation or emit a factual aggregate report for one tracker file."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "report"))
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    data = load_tracker(args.path)
    errors = validate_tracker(data)
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    if args.command == "report":
        print(json.dumps(summarize_tracker(data), ensure_ascii=False, indent=2))
    else:
        print("PASS: evidence links, requirement coverage, and application stages are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
