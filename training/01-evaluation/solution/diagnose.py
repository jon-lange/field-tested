#!/usr/bin/env python3
"""Three checks on the checks.  python3 diagnose.py

Every number this prints is computed from the lab in front of you. Nothing is
quoted from anywhere else, which is the same rule the reading list follows and
the reason its figures are worth anything.
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import subject  # noqa: E402
import gate  # noqa: E402


def probe_absence_test() -> None:
    """Is the credential check watching redaction, or watching nothing?

    Break redaction on purpose and re-run the check. A check that still passes
    with the guarded behaviour destroyed was never observing it.
    """
    print("1. the credential check")
    verdict, _ = gate.check_no_credential_leak()
    print(f"   as shipped:            {verdict}")

    original = subject.Summariser.redact
    subject.Summariser.redact = lambda self, text: text  # a no-op
    try:
        verdict, _ = gate.check_no_credential_leak()
    finally:
        subject.Summariser.redact = original

    if verdict == gate.PASS:
        print(f"   with redaction OFF:    {verdict}  <-- VACUOUS")
        print("   The check passes whether redaction works or not, so it is not")
        print("   evidence that redaction works. Nothing is logged at all:")
        print(f"   SUMMARY_LOGGING_ENABLED = {subject.SUMMARY_LOGGING_ENABLED}.")
        print("   The property is fine. The evidence for it was destroyed, and a")
        print("   green tick looks identical either way.")
    else:
        print(f"   with redaction OFF:    {verdict}  (the check is live)")
    print()


def probe_judge() -> None:
    """Does the judge discriminate, and is it stable?

    A judge that returns the same score for everything passes every threshold
    and separates nothing. Saturation is invisible from a single score.
    """
    print("2. the quality judge")
    good = subject.judge_quality("A clear, accurate, complete summary.")
    poor = subject.judge_quality("asdf")
    empty = subject.judge_quality("")
    print(f"   good summary:  {good}/5")
    print(f"   poor summary:  {poor}/5")
    print(f"   empty string:  {empty}/5")

    if good == poor == empty:
        print("   <-- NO SIGNAL. Identical scores for inputs of obviously different")
        print("   quality. The 4-or-better threshold is satisfied by anything at all,")
        print("   so the check cannot fail and therefore cannot inform a release.")
        print("   Check discrimination BEFORE trusting a verdict, not after.")
    else:
        print("   the judge discriminates between these inputs")
    print()


def probe_scorecard(steps: int = 20) -> None:
    """How much of the weighting space would pick the other candidate?

    The weights were never ratified. So the honest question is not 'who wins'
    but 'who wins across the weightings a reasonable person might defend'.
    """
    print("3. the weighted scorecard")
    shipped = subject.pick_winner(subject.WEIGHTS)
    print(f"   shipped weights pick:  {shipped}")

    dims = subject.DIMENSIONS
    flips = total = 0
    # Every weighting on a simplex grid: non-negative, summing to 1.
    for combo in itertools.product(range(steps + 1), repeat=len(dims) - 1):
        if sum(combo) > steps:
            continue
        parts = list(combo) + [steps - sum(combo)]
        weights = {d: p / steps for d, p in zip(dims, parts)}
        total += 1
        if subject.pick_winner(weights) != shipped:
            flips += 1

    share = 100 * flips / total if total else 0
    print(f"   weightings examined:   {total:,}")
    print(f"   picking the other one: {flips:,}  ({share:.1f}%)")
    print(f"   <-- {share:.1f}% of the weighting space reverses this release decision.")
    print("   The verdict is a property of an unratified weighting, not of the")
    print("   candidates. Report the share, or get the weights ratified by whoever")
    print("   owns the tradeoff. Do not report the winner alone.")
    print()


def main() -> int:
    print("diagnosing the gate — every figure below is computed from this lab\n")
    probe_absence_test()
    probe_judge()
    probe_scorecard()
    print("Three green checks. None of them evidence of what it appeared to show.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
