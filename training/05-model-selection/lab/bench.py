"""Three candidate models, one benchmark, and the numbers behind the decision.

Deterministic, standard library, no calls. Generic domain — classifying support
tickets for a build-tooling product.
"""

from __future__ import annotations

# Headline benchmark accuracy. Close enough that the decision looks like cost.
MODELS = {
    "atlas-large":  {"accuracy": 0.912, "cost_per_1k": 9.00,  "p95_ms": 2400},
    "atlas-small":  {"accuracy": 0.907, "cost_per_1k": 0.90,  "p95_ms": 700},
    "beacon-mid":   {"accuracy": 0.905, "cost_per_1k": 2.40,  "p95_ms": 1100},
}

# The same benchmark, broken out. The headline is a mean over these.
SLICES = {
    "billing":        {"weight": 0.10, "atlas-large": 0.90, "atlas-small": 0.41, "beacon-mid": 0.88},
    "build-failure":  {"weight": 0.55, "atlas-large": 0.92, "atlas-small": 0.97, "beacon-mid": 0.90},
    "access-request": {"weight": 0.20, "atlas-large": 0.91, "atlas-small": 0.93, "beacon-mid": 0.92},
    "feature-idea":   {"weight": 0.15, "atlas-large": 0.91, "atlas-small": 0.90, "beacon-mid": 0.93},
}

# Measured alongside accuracy and reported nowhere. A ticket the model declines
# to classify goes to a human, which is a cost the accuracy number cannot see.
REFUSAL = {"atlas-large": 0.01, "atlas-small": 0.14, "beacon-mid": 0.02}

# What the benchmark does not contain at all.
UNCOVERED = ["tickets in a language other than English", "tickets over 4k tokens"]


def headline(model: str) -> float:
    return sum(s["weight"] * s[model] for s in SLICES.values())
