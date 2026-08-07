"""The system under evaluation: a docs-summarisation feature behind a release gate.

Generic on purpose. Nothing here is domain-specific, because a lab written
against a particular vertical teaches that vertical rather than the technique.

You are not meant to read this file first. Run `python3 gate.py`, watch it go
green, and then come back and work out why you should not believe it.
"""

from __future__ import annotations

# A rollout flag. Off in this environment, as flags routinely are.
SUMMARY_LOGGING_ENABLED = False

API_TOKEN = "tok_live_9f3a2c8b1d"


class Summariser:
    """Summarises internal docs. Redacts credentials before anything is logged."""

    def __init__(self) -> None:
        self.log_lines: list[str] = []

    def redact(self, text: str) -> str:
        return text.replace(API_TOKEN, "[REDACTED]")

    def summarise(self, document: str) -> str:
        summary = f"Summary of {len(document.split())} words. Token: {API_TOKEN}"
        self._log(summary)
        return summary

    def _log(self, summary: str) -> None:
        # The redaction is real and correct. Whether it ever runs is another
        # question, and it is the question the suite does not ask.
        if SUMMARY_LOGGING_ENABLED:
            self.log_lines.append(self.redact(summary))

    def logged(self) -> str:
        return "\n".join(self.log_lines)


# ---------------------------------------------------------------- candidates
# Two competing configurations. The release gate has to pick one.

CANDIDATES = {
    "candidate-a": {
        "accuracy": 8.0, "latency": 9.0, "cost": 9.0,
        "coverage": 4.0, "readability": 8.0, "safety": 5.0,
    },
    "candidate-b": {
        "accuracy": 7.0, "latency": 5.0, "cost": 5.0,
        "coverage": 9.0, "readability": 6.0, "safety": 9.0,
    },
}

DIMENSIONS = ["accuracy", "latency", "cost", "coverage", "readability", "safety"]

# Nobody ratified these. Someone picked them in a planning meeting and they have
# gated every release since.
WEIGHTS = {
    "accuracy": 0.25, "latency": 0.25, "cost": 0.20,
    "coverage": 0.10, "readability": 0.10, "safety": 0.10,
}


def weighted_score(candidate: str, weights: dict[str, float]) -> float:
    scores = CANDIDATES[candidate]
    return sum(scores[d] * weights[d] for d in DIMENSIONS)


def pick_winner(weights: dict[str, float]) -> str:
    return max(CANDIDATES, key=lambda c: weighted_score(c, weights))


# -------------------------------------------------------------------- judge
# A model-as-judge, stubbed so the lab runs offline and deterministically. The
# behaviour it stands in for is real and was measured: see the reading list.


def judge_quality(summary: str) -> int:
    """Score a summary 1-5 on overall quality."""
    # A real judge would call a model here. This one reproduces, exactly, the
    # response distribution that disqualified two of three judges in a real run.
    return 5
