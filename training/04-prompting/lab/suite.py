"""Two prompt versions, one eval set, and the numbers that decided the rollout.

Deterministic and generated in process. The model is stubbed: what matters here
is the shape of the comparison, not the completion.

Generic domain — extracting fields from build logs.
"""

from __future__ import annotations

# Four classes of input. The eval set is not balanced, because eval sets rarely
# are: they grow by adding whatever failed last, and nobody rebalances.
CLASSES = {
    "routine": 120,
    "multiline": 40,
    "truncated": 30,
    "non-english": 10,
}

# Per-class accuracy for each prompt version. v2 is a real improvement on the
# common case and a collapse on one rare one.
SCORES = {
    "v1": {"routine": 0.86, "multiline": 0.71, "truncated": 0.64, "non-english": 0.80},
    "v2": {"routine": 0.94, "multiline": 0.83, "truncated": 0.72, "non-english": 0.10},
}

PROMPTS = {
    "v1": "Extract the failing step and the exit code from this build log.",
    "v2": ("Extract the failing step and the exit code from this build log. "
           "Respond in English. Use the exact step name as written."),
}


def overall(version: str) -> float:
    total = sum(CLASSES.values())
    return sum(SCORES[version][c] * n for c, n in CLASSES.items()) / total


def per_class(version: str) -> dict[str, float]:
    return dict(SCORES[version])


# ------------------------------------------------------- the system instruction
#
# Added in v2 and never tested. There is no eval case that would fail if the
# model ignored it entirely.

SYSTEM_RULE = "Never include the raw log line in your response."


def response(version: str, item_class: str) -> str:
    """Stubbed. v2 obeys the rule most of the time and not always — which is the
    ordinary case, and is invisible unless something checks."""
    if version == "v1":
        return "step: compile · exit 2 · raw: `[ERROR] compile failed at line 44`"
    if item_class == "truncated":
        # Under truncation the model falls back to quoting the log.
        return "step: compile · exit 2 · raw: `[ERROR] compile failed at line 44`"
    return "step: compile · exit 2"


EVAL_CASES = [c for c, n in CLASSES.items() for _ in range(n)]
