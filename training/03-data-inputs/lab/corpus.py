"""The document corpus and the retrieval over it.

Deterministic, standard library, no model. The generator is stubbed the same way
module 01 stubs its judge: what matters here is what reaches the model, not what
the model does with it.

Generic domain on purpose — a build-cache service. A lab written against a real
vertical teaches that vertical instead of the technique.

Do not read this first. Run `python3 ask.py`, watch every question get a
confident answer, and then work out which answers are grounded in anything.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------- the corpus
#
# Five documents. Two of them are the same runbook: one is the original, the
# other is a copy someone pasted into a second wiki space and lightly edited.
# Nothing in the pipeline knows that.

DOCS = {
    "runbook-cache-evictions": """
        Cache evictions are triggered when the shared tier exceeds its memory
        budget. The eviction policy is least-recently-used. Operators can raise
        the budget in the cluster config. Evictions are logged to the audit
        stream.
    """,
    "runbook-cache-evictions-copy": """
        Cache evictions trigger when the shared tier goes over its memory
        budget. The eviction policy is least-recently-used. Operators may raise
        the budget in cluster config. Evictions get logged to the audit stream.
    """,
    "runbook-cache-evictions-archive": """
        Cache evictions are triggered when the shared tier exceeds its memory
        budget. Policy is least-recently-used. The budget is raised in the
        cluster config. Evictions are written to the audit stream.
    """,
    "onboarding-build-agents": """
        Build agents register with the scheduler on start. Each agent reports a
        heartbeat every thirty seconds. An agent that misses three consecutive
        heartbeats is marked unhealthy and drained.
    """,
    "policy-artifact-retention": """
        Build artifacts are retained for ninety days. Retention is enforced by a
        nightly sweep. Artifacts referenced by a pinned release are exempt from
        the sweep and retained indefinitely.
    """,
}

# Chunking. Fixed width, no overlap — the default in more pipelines than anyone
# would like to admit.
CHUNK_CHARS = 180


def chunks() -> list[tuple[str, str]]:
    out = []
    for name, body in DOCS.items():
        text = " ".join(body.split())
        for i in range(0, len(text), CHUNK_CHARS):
            out.append((name, text[i:i + CHUNK_CHARS]))
    return out


CHUNKS = chunks()


def retrieve(question: str, k: int = 3) -> list[tuple[str, str]]:
    """Keyword overlap, the honest version of a bad retriever.

    Returns the k best chunks. Note what it does when nothing matches at all.
    """
    words = set(re.findall(r"[a-z]{4,}", question.lower()))
    scored = []
    for name, chunk in CHUNKS:
        overlap = len(words & set(re.findall(r"[a-z]{4,}", chunk.lower())))
        if overlap:
            scored.append((overlap, name, chunk))
    scored.sort(key=lambda s: (-s[0], s[1]))
    return [(name, chunk) for _, name, chunk in scored[:k]]


def answer(question: str, context: list[tuple[str, str]]) -> str:
    """Stands in for a model. Reproduces the behaviour that matters: it composes
    a fluent answer from whatever it is given, including nothing."""
    if not context:
        # The generator does not refuse. Very few do, unprompted.
        return ("Based on the available documentation, this is handled "
                "automatically by the platform.")
    joined = " ".join(c for _, c in context)
    for sentence in re.split(r"(?<=\.)\s+", joined):
        if set(re.findall(r"[a-z]{4,}", question.lower())) & set(
                re.findall(r"[a-z]{4,}", sentence.lower())):
            return sentence.strip()
    return joined.split(".")[0].strip() + "."


QUESTIONS = [
    "What triggers cache evictions?",
    "How long are build artifacts retained?",
    "What happens when an agent misses heartbeats?",
    "What is the escalation path for a failed nightly sweep?",
]
