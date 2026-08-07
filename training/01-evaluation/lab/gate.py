#!/usr/bin/env python3
"""The release gate. Run it:  python3 gate.py

Three checks. All three pass. The feature ships.

Your job is to work out why you should not believe any of them — without
changing what the checks assert. Each one is a real, common shape, and each
one has been measured failing in the wild.
"""

from __future__ import annotations

import subject

PASS = "PASS"
FAIL = "FAIL"


def check_no_credential_leak() -> tuple[str, str]:
    """Nothing we log may contain the API token."""
    s = subject.Summariser()
    s.summarise("an internal document about the build cache")
    leaked = subject.API_TOKEN in s.logged()
    return (FAIL if leaked else PASS), "no credential found in logged output"


def check_quality_threshold() -> tuple[str, str]:
    """A model judge scores summary quality. We require 4 or better."""
    s = subject.Summariser()
    summary = s.summarise("an internal document about the build cache")
    score = subject.judge_quality(summary)
    return (PASS if score >= 4 else FAIL), f"judge scored {score}/5"


def check_candidate_selection() -> tuple[str, str]:
    """The weighted scorecard picks the configuration we ship."""
    winner = subject.pick_winner(subject.WEIGHTS)
    score = subject.weighted_score(winner, subject.WEIGHTS)
    return PASS, f"{winner} selected, weighted score {score:.2f}"


CHECKS = [
    ("no credential leak", check_no_credential_leak),
    ("quality threshold", check_quality_threshold),
    ("candidate selection", check_candidate_selection),
]


def main() -> int:
    print("release gate\n")
    failures = 0
    for name, check in CHECKS:
        verdict, detail = check()
        if verdict == FAIL:
            failures += 1
        print(f"  {verdict}  {name:<24} {detail}")

    print()
    if failures:
        print(f"  BLOCKED — {failures} check(s) failed")
        return 1
    print("  all checks green — cleared to ship")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
