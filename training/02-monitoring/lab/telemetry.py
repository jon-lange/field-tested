"""Thirty days of telemetry for a docs-summarisation service, plus the alert
rules watching it.

Deterministic and generated in process — no random, no fixtures, no network. Two
runs produce identical numbers, which is what lets the diagnosis quote them.

Same generic domain as module 01, on purpose. A lab written against a real
vertical teaches that vertical instead of the technique.

Do not read this first. Run `python3 dashboard.py`, see everything green, and
then work out what it is not showing you.
"""

from __future__ import annotations

DAYS = 30

# Traffic splits by document size. The long tail is small and, as usual, is
# where the difficulty lives.
SEGMENTS = {
    "short": {"share": 0.74, "base_success": 0.995},
    "medium": {"share": 0.23, "base_success": 0.988},
    "long": {"share": 0.03, "base_success": 0.710},
}

REQUESTS_PER_DAY = 4000


def requests(day: int, segment: str) -> int:
    return round(REQUESTS_PER_DAY * SEGMENTS[segment]["share"])


def successes(day: int, segment: str) -> int:
    """Steady per segment. Nothing here degrades over time — the long segment
    was always this bad, which is why nobody noticed it start."""
    return round(requests(day, segment) * SEGMENTS[segment]["base_success"])


def success_rate_overall(day: int) -> float:
    total = sum(requests(day, s) for s in SEGMENTS)
    good = sum(successes(day, s) for s in SEGMENTS)
    return good / total


def success_rate(day: int, segment: str) -> float:
    return successes(day, segment) / requests(day, segment)


def quality_score(day: int) -> float:
    """Judge-scored summary quality, 1-5. Flat all month."""
    return 4.6


def refusal_rate(day: int) -> float:
    """The share of requests the guardrail declined.

    A guardrail was tightened on day 8. Nothing on the dashboard charts this
    series, so the only way to see it is to go looking.
    """
    if day < 8:
        return 0.02
    ramp = min((day - 7) / 6, 1.0)
    return 0.02 + ramp * 0.16


# --------------------------------------------------------------- alert rules
#
# A rule fires when its metric breaches the threshold. A rule whose metric
# does not exist has nothing to breach.

METRICS_EMITTED = {
    "summariser.success_rate",
    "summariser.quality_score",
    "summariser.refusal_rate",
    "summariser.latency_p50_ms",
}

ALERTS = [
    {
        "name": "success rate below 98%",
        "metric": "summariser.success_rate",
        "op": "<",
        "threshold": 0.98,
    },
    {
        "name": "quality below 4.0",
        "metric": "summariser.quality_score",
        "op": "<",
        "threshold": 4.0,
    },
    {
        # Renamed by the pipeline refactor in week two: the emitter now writes
        # summariser.latency_p50_ms. The rule was never updated. It queries a
        # series that does not exist, gets nothing back, and nothing is not
        # greater than 3000.
        "name": "latency p50 above 3s",
        "metric": "summarizer.latency_p50",
        "op": ">",
        "threshold": 3000,
    },
]


def series(metric: str) -> list[float]:
    """Values for a metric across the window. An unknown metric returns no
    data — the same shape a real query returns for a series nobody writes."""
    if metric not in METRICS_EMITTED:
        return []
    if metric == "summariser.success_rate":
        return [success_rate_overall(d) for d in range(DAYS)]
    if metric == "summariser.quality_score":
        return [quality_score(d) for d in range(DAYS)]
    if metric == "summariser.refusal_rate":
        return [refusal_rate(d) for d in range(DAYS)]
    if metric == "summariser.latency_p50_ms":
        return [1800.0 + 40 * (d % 5) for d in range(DAYS)]
    return []


def evaluate(alert: dict) -> tuple[bool, str]:
    """Does this alert fire? Returns (fired, detail)."""
    values = series(alert["metric"])
    if not values:
        # No data, no breach. This is the branch that matters.
        return False, "no breach"
    worst = min(values) if alert["op"] == "<" else max(values)
    fired = worst < alert["threshold"] if alert["op"] == "<" else worst > alert["threshold"]
    return fired, f"worst {worst:.4g} vs {alert['op']} {alert['threshold']}"
