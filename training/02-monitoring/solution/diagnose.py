#!/usr/bin/env python3
"""Three questions the dashboard does not ask.  python3 diagnose.py

Every figure is computed from the lab. Nothing is quoted from anywhere else.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import telemetry as t  # noqa: E402


def probe_alerts() -> None:
    """Which alerts *could* fire?

    An alert that has never fired is either watching a healthy system or
    watching nothing, and from the dashboard those are the same picture.
    """
    print("1. can each alert fire at all?")
    dead = 0
    for alert in t.ALERTS:
        values = t.series(alert["metric"])
        if not values:
            dead += 1
            print(f"   DEAD   {alert['name']}")
            print(f"          queries {alert['metric']!r}, which nothing emits.")
            near = [m for m in t.METRICS_EMITTED if m.split(".")[-1].startswith(
                alert["metric"].split(".")[-1][:7])]
            if near:
                print(f"          emitted instead: {near[0]}")
        else:
            print(f"   live   {alert['name']}  ({len(values)} points)")
    if dead:
        print(f"   <-- {dead} of {len(t.ALERTS)} alerts cannot fire. They have never")
        print("   fired, they never will, and on the dashboard that is indistinguishable")
        print("   from a system that has never breached them.")
        print("   Fire every rule deliberately at least once. An alert nobody has")
        print("   watched go red is not monitoring, it is decoration.")
    print()


def probe_aggregate() -> None:
    """Does the headline number describe every segment, or hide one?"""
    print("2. does the average describe anyone?")
    overall = t.success_rate_overall(0)
    print(f"   overall success rate:  {overall:.2%}   (alert threshold 98%)")
    worst_name, worst_rate, worst_share = None, 1.0, 0.0
    for seg in t.SEGMENTS:
        rate = t.success_rate(0, seg)
        share = t.SEGMENTS[seg]["share"]
        print(f"     {seg:<7} {share:>5.0%} of traffic   {rate:.2%}")
        if rate < worst_rate:
            worst_name, worst_rate, worst_share = seg, rate, share

    failing = round(t.REQUESTS_PER_DAY * worst_share * (1 - worst_rate))
    print(f"   <-- '{worst_name}' fails {1 - worst_rate:.1%} of the time and is {worst_share:.0%}")
    print(f"   of traffic, so it moves the overall number by roughly")
    print(f"   {worst_share * (1 - worst_rate):.2%} — inside the rounding of a green panel.")
    print(f"   That is about {failing:,} failed requests a day that nothing reports.")
    print("   Alert on the worst segment, not the mean. Averaging is how a failure")
    print("   stops looking like one.")
    print()


def probe_unwatched() -> None:
    """Is anything moving that no panel charts?"""
    print("3. what moved that nothing charts?")
    charted = {a["metric"] for a in t.ALERTS} | {
        "summariser.success_rate", "summariser.quality_score",
        "summariser.latency_p50_ms",
    }
    unwatched = sorted(t.METRICS_EMITTED - charted)

    q_first, q_last = t.quality_score(0), t.quality_score(t.DAYS - 1)
    print(f"   quality      {q_first:.2f} -> {q_last:.2f}   (charted, flat)")
    for metric in unwatched:
        values = t.series(metric)
        print(f"   {metric.split('.')[-1]:<12} {values[0]:.2%} -> {values[-1]:.2%}"
              f"   (emitted, on no panel, no alert)")
        change = values[-1] / values[0]
        print(f"   <-- up {change:.0f}x over the window while quality did not move.")
    print("   A composite that folds refusal into quality is dominated by quality:")
    print("   the score barely shifts while the system quietly declines more work,")
    print("   and the dashboard stays green. Keep two numbers. Gate on both.")
    print()


def main() -> int:
    print("diagnosing the dashboard — every figure computed from this lab\n")
    probe_alerts()
    probe_aggregate()
    probe_unwatched()
    print("Three green panels, no alerts firing, and none of it evidence that the")
    print("system is healthy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
