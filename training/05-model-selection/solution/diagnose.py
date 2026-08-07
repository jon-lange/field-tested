#!/usr/bin/env python3
"""Three questions the benchmark does not answer.  python3 diagnose.py

Every figure is computed from the lab.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import bench  # noqa: E402


def probe_slices() -> None:
    print("1. does 0.7% mean they behave the same?")
    names = list(bench.MODELS)
    print(f"   {'slice':<17}{'wt':>5}" + "".join(f"{n:>14}" for n in names))
    worst = None
    for s, d in bench.SLICES.items():
        row = "".join(f"{d[n]:>13.0%} " for n in names)
        print(f"   {s:<17}{d['weight']:>4.0%} {row}")
        spread = max(d[n] for n in names) - min(d[n] for n in names)
        if worst is None or spread > worst[1]:
            worst = (s, spread, d)
    s, spread, d = worst
    low = min(names, key=lambda n: d[n])
    print()
    print(f"   <-- on '{s}' the spread is {spread:.0%}, not 0.7%.")
    print(f"   {low} scores {d[low]:.0%} there. It is {d['weight']:.0%} of volume, so the")
    print(f"   headline absorbs it: {(1 - d[low]) * d['weight']:.1%} off a mean that")
    print("   three models share. Same number, different systems.")
    print("   Compare per slice. The mean is a claim about a weighting.")
    print()


def probe_unmeasured() -> None:
    print("2. what was measured and never reported?")
    print(f"   {'model':<14}{'accuracy':>10}{'refusal':>10}{'handled':>10}")
    for m in bench.MODELS:
        acc, ref = bench.headline(m), bench.REFUSAL[m]
        print(f"   {m:<14}{acc:>9.1%}{ref:>10.0%}{acc * (1 - ref):>9.1%}")
    worst = max(bench.REFUSAL, key=bench.REFUSAL.get)
    print()
    print(f"   <-- {worst} declines {bench.REFUSAL[worst]:.0%} of tickets. Those are correct")
    print("   refusals, not errors, so accuracy never moves — every one is a")
    print("   ticket a human now handles. Rank on tickets actually resolved and")
    print("   the ordering changes.")
    print()


def probe_cost() -> None:
    print("3. cost per call, or cost per resolved ticket?")
    print(f"   {'model':<14}{'$/1k calls':>12}{'$/1k resolved':>15}")
    ranking = []
    for m, d in bench.MODELS.items():
        resolved = bench.headline(m) * (1 - bench.REFUSAL[m])
        eff = d["cost_per_1k"] / resolved
        ranking.append((eff, m))
        print(f"   {m:<14}{d['cost_per_1k']:>12.2f}{eff:>15.2f}")
    ranking.sort()
    print()
    print(f"   <-- {ranking[0][1]} is still cheapest per resolved ticket, but the gap")
    print(f"   narrows: the {bench.MODELS[ranking[0][1]]['cost_per_1k']:.2f} headline hides "
          f"{bench.REFUSAL[ranking[0][1]]:.0%} going to a queue")
    print("   whose cost is a salary, and does not appear on this table at all.")
    print()
    print("   And what the benchmark never covered:")
    for u in bench.UNCOVERED:
        print(f"     - {u}")
    print("   No score here is evidence about those, in either direction.")
    print()


def main() -> int:
    print("diagnosing the choice — every figure computed from this lab\n")
    probe_slices()
    probe_unmeasured()
    probe_cost()
    print("Three models within 0.7%, and they are not interchangeable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
