#!/usr/bin/env python3
"""The dashboard.  python3 dashboard.py

Thirty days. Three alerts, none firing. Every panel green.

Your job is to work out what it is not showing you — without changing a
threshold or relaxing a rule. Each of the three failures below is ordinary, and
each one leaves a dashboard that looks exactly like a healthy system.
"""

from __future__ import annotations

import telemetry as t


def bar(value: float, width: int = 28) -> str:
    filled = round(value * width)
    return "#" * filled + "." * (width - filled)


def main() -> int:
    print("summariser · last 30 days\n")

    overall = sum(t.success_rate_overall(d) for d in range(t.DAYS)) / t.DAYS
    quality = sum(t.quality_score(d) for d in range(t.DAYS)) / t.DAYS
    latency = sum(t.series("summariser.latency_p50_ms")) / t.DAYS

    print("  PANELS")
    print(f"    success rate      {overall:7.2%}   {bar(overall)}")
    print(f"    quality (1-5)     {quality:7.2f}   {bar(quality / 5)}")
    print(f"    latency p50       {latency:6.0f}ms   {bar(latency / 5000)}")
    print()

    print("  ALERTS")
    firing = 0
    for alert in t.ALERTS:
        fired, detail = t.evaluate(alert)
        firing += fired
        print(f"    {'FIRING' if fired else '  ok  '}  {alert['name']:<28} {detail}")
    print()

    if firing:
        print(f"  {firing} alert(s) firing")
        return 1
    print("  all panels green, no alerts firing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
