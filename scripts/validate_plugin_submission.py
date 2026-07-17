#!/usr/bin/env python3
"""Validate Novelist's public-submission payload and existing test suites."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "novelist"
MANIFEST = PLUGIN / ".codex-plugin" / "plugin.json"
TEST_CASES = PLUGIN / "submission" / "test-cases.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def run(*command: str) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(command, cwd=ROOT, env=environment, check=True)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    cases = json.loads(TEST_CASES.read_text())
    interface = manifest["interface"]

    require(manifest["license"] == "MIT", "manifest license must be MIT")
    require(manifest["author"]["name"] == "Changkyun Kim", "publisher name mismatch")
    require(manifest["author"]["email"] == "comfuture@gmail.com", "publisher email mismatch")
    require(interface["category"] == "Productivity", "category must be Productivity")
    require(bool(interface["shortDescription"]), "short description is required")
    require(bool(interface["longDescription"]), "long description is required")
    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        require(interface[key].startswith("https://"), f"{key} must use HTTPS")
    for key in ("composerIcon", "logo"):
        require((PLUGIN / interface[key]).is_file(), f"missing asset: {interface[key]}")

    require(len(cases["positive"]) == 5, "submission requires exactly five positive cases")
    require(len(cases["negative"]) == 3, "submission requires exactly three negative cases")
    all_cases = cases["positive"] + cases["negative"]
    require(len({case["id"] for case in all_cases}) == 8, "test case IDs must be unique")
    for case in all_cases:
        for key in ("prompt", "expectedBehavior", "validation"):
            require(bool(case.get(key)), f"{case['id']} is missing {key}")
        require((ROOT / case["validation"]).is_file(), f"missing validation evidence for {case['id']}")

    run(sys.executable, "scripts/sync_novelist_plugin.py", "--check")
    for tests in (
        "plugins/novelist/skills/create-novel-project/tests",
        "plugins/novelist/skills/novel-story-telling/tests",
        "plugins/novelist/skills/publish-novel/tests",
    ):
        run(sys.executable, "-m", "unittest", "discover", "-s", tests, "-p", "test_*.py")

    print("Novelist public-submission payload is valid (5 positive, 3 negative).")


if __name__ == "__main__":
    main()
