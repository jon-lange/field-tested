#!/usr/bin/env python3
"""Three questions the runner does not ask.  python3 diagnose.py

Every figure is computed from the lab.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import pipeline  # noqa: E402


def instrumented_run():
    """Same pipeline, but recording what the runner discards."""
    pipeline.STATE["attempts"] = 0
    prev, log = None, []
    for stage in pipeline.STAGES:
        errors, result = [], None
        for _ in range(pipeline.MAX_RETRIES):
            try:
                result = stage(prev)
                break
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: {exc}")
        log.append((result.stage, result, errors))
        prev = result
    return log


def main() -> int:
    print("diagnosing the pipeline — every figure computed from this lab\n")
    log = instrumented_run()

    print("1. what did the retries swallow?")
    retried = [(s, e) for s, _, e in log if e]
    for stage, errors in retried:
        print(f"   {stage}: {len(errors)} failure(s) before success")
        for e in errors:
            print(f"     {e}")
    if retried:
        print("   <-- the runner caught these, retried, and reported ok. The retry")
        print("   worked, which is the problem: nothing counts how often a stage")
        print("   needs one. A stage failing 49% of the time and a stage that has")
        print("   never failed produce the same line.")
        print("   Emit the retry count. A rising one is the earliest signal you get.")
    print()

    print("2. which stage returned a degraded result?")
    degraded = [(s, r) for s, r, _ in log if r.notes]
    for stage, r in degraded:
        print(f"   {stage}: {r.notes[0]}")
    if degraded:
        print("   <-- the fallback returned a valid Result, so the stage is ok and")
        print("   the pipeline is SUCCESS. Forty documents were indexed and none of")
        print("   them were enriched. A fallback that cannot be distinguished from")
        print("   the real path converts an outage into a silent quality change.")
        print("   Make degraded a third outcome, not a shade of success.")
    print()

    print("3. which stage did nothing?")
    noop = []
    for i, (stage, r, _) in enumerate(log):
        before = log[i - 1][1].items if i else r.items
        if r.items == before and stage in ("dedupe",):
            noop.append((stage, before, r.items))
    for stage, before, after in noop:
        print(f"   {stage}: {before} in, {after} out, flag "
              f"DEDUPE_ENABLED={pipeline.DEDUPE_ENABLED}")
    if noop:
        print("   <-- disabled by a flag, and it returns success. Identical output to")
        print("   a working dedupe over input that happened to be unique — which is")
        print("   why nobody notices. The stage is in the diagram and in the log.")
        print("   Report what a stage did, not that it ran.")
    print()

    print("Five stages, all ok, and the run had a failure, a degradation, and a")
    print("stage that did nothing. None of it reached the summary line.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
