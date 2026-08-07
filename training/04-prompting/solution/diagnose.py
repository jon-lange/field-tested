#!/usr/bin/env python3
"""Three questions the A/B does not ask.  python3 diagnose.py

Every figure is computed from the lab.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import suite  # noqa: E402


def probe_per_class() -> None:
    """Did v2 improve everywhere, or improve on average?"""
    print("1. who got better, and who got worse?")
    total = sum(suite.CLASSES.values())
    print(f"   {'class':<14}{'share':>7}{'v1':>8}{'v2':>8}{'delta':>9}")
    regressions = []
    for c, n in suite.CLASSES.items():
        a, b = suite.SCORES["v1"][c], suite.SCORES["v2"][c]
        mark = "  <--" if b < a else ""
        print(f"   {c:<14}{n/total:>6.0%}{a:>8.0%}{b:>8.0%}{b-a:>+9.0%}{mark}")
        if b < a:
            regressions.append((c, a, b, n / total))

    for c, a, b, share in regressions:
        cost = (a - b) * share
        print()
        print(f"   <-- '{c}' fell {a:.0%} to {b:.0%}, a {a-b:.0%} collapse.")
        print(f"   It is {share:.0%} of the eval set, so it moves the headline by")
        print(f"   {cost:.1%} — against a {suite.overall('v2') - suite.overall('v1'):+.1%} total.")
        print("   The win is real and so is the regression. Only one is reported.")
    print()


def probe_eval_balance() -> None:
    """Does the eval set weight classes the way production does?"""
    print("2. what is the eval set actually weighting?")
    total = sum(suite.CLASSES.values())
    biggest = max(suite.CLASSES.items(), key=lambda kv: kv[1])
    smallest = min(suite.CLASSES.items(), key=lambda kv: kv[1])
    ratio = biggest[1] / smallest[1]
    print(f"   {biggest[0]}: {biggest[1]} cases · {smallest[0]}: {smallest[1]} cases"
          f"  ({ratio:.0f}x)")
    print(f"   <-- a single aggregate over an unbalanced set is a weighted score,")
    print("   and nobody ratified these weights. They are whatever the eval set")
    print("   happened to accumulate as failures were added and never rebalanced.")
    print("   Report per class. If you must have one number, say whose it is.")
    print()


def probe_untested_rule() -> None:
    """v2 added an instruction. Does anything check it is followed?"""
    print("3. the instruction nobody tests")
    print(f"   system rule: {suite.SYSTEM_RULE!r}")
    violations = []
    for c in suite.CLASSES:
        reply = suite.response("v2", c)
        if "raw:" in reply:
            violations.append(c)
    print(f"   classes where v2 still includes the raw line: "
          f"{violations if violations else 'none'}")
    print("   <-- no eval case fails when this rule is ignored, so the accuracy")
    print("   number is identical whether the model obeys it or not. An")
    print("   instruction with no test is a preference, and it holds exactly as")
    print("   often as the model happens to comply.")
    print("   Add the negative case: an input that would tempt a violation.")
    print()


def main() -> int:
    print("diagnosing the A/B — every figure computed from this lab\n")
    probe_per_class()
    probe_eval_balance()
    probe_untested_rule()
    print("v2 is better. It is also a regression, and it ships an untested")
    print("instruction. The headline said none of that.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
