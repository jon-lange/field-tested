#!/usr/bin/env python3
"""The pipeline runner.  python3 run.py

Five stages, all green, forty documents in and forty out.

Your job is to work out what "success" is covering for — without changing a
stage.
"""

from __future__ import annotations

import pipeline


def main() -> int:
    print("release-notes ingest\n")
    prev, results = None, []
    for stage in pipeline.STAGES:
        for _ in range(pipeline.MAX_RETRIES):
            try:
                prev = stage(prev)
                break
            except Exception:
                continue
        results.append(prev)
        print(f"  ok    {prev.stage:<10} {prev.items:>3} items")

    print()
    print(f"  pipeline SUCCESS — {len(results)}/{len(pipeline.STAGES)} stages, "
          f"{results[-1].items} documents indexed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
