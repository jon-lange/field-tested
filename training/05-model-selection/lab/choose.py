#!/usr/bin/env python3
"""The model decision.  python3 choose.py

Three candidates, within half a point of each other. One is ten times cheaper.

Your job is to work out whether that is the decision — without changing the
benchmark.
"""

from __future__ import annotations

import bench


def main() -> int:
    print("model selection · ticket classification\n")
    print(f"  {'model':<14}{'accuracy':>10}{'$/1k':>9}{'p95':>9}")
    for m, d in bench.MODELS.items():
        print(f"  {m:<14}{d['accuracy']:>9.1%}{d['cost_per_1k']:>9.2f}{d['p95_ms']:>8}ms")
    print()

    best = max(bench.MODELS, key=lambda m: bench.MODELS[m]["accuracy"])
    spread = (bench.MODELS[best]["accuracy"]
              - min(d["accuracy"] for d in bench.MODELS.values()))
    cheap = min(bench.MODELS, key=lambda m: bench.MODELS[m]["cost_per_1k"])
    print(f"  accuracy spread: {spread:.1%} — inside the noise anyone would accept")
    print(f"  cheapest: {cheap} at ${bench.MODELS[cheap]['cost_per_1k']:.2f}/1k, "
          f"{bench.MODELS[best]['cost_per_1k'] / bench.MODELS[cheap]['cost_per_1k']:.0f}x less")
    print()
    print(f"  Recommend {cheap}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
