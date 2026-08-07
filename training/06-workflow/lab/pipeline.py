"""A five-stage document-processing pipeline and the runner that reports on it.

Deterministic, standard library. Generic domain — ingesting release notes.

Every stage returns a result. The runner reports whether the pipeline
succeeded. Those are not the same question, and this file is where the
difference lives.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Result:
    stage: str
    ok: bool = True
    items: int = 0
    notes: list[str] = field(default_factory=list)


STATE: dict[str, object] = {"attempts": 0}


def fetch(_: None) -> Result:
    return Result("fetch", items=40)


def parse(prev: Result) -> Result:
    """Fails once, succeeds on retry. The retry is the point."""
    STATE["attempts"] = int(STATE["attempts"]) + 1
    if STATE["attempts"] == 1:
        raise RuntimeError("malformed document at offset 12")
    return Result("parse", items=prev.items)


def enrich(prev: Result) -> Result:
    """The enrichment service is down. The fallback returns the input
    unenriched, which is a valid Result and a degraded one."""
    try:
        raise ConnectionError("enrichment service unreachable")
    except ConnectionError as exc:
        return Result("enrich", items=prev.items,
                      notes=[f"fallback: passthrough ({exc})"])


def dedupe(prev: Result) -> Result:
    """Guarded by a flag that defaults off. Returns success having done
    nothing — which is exactly what a working dedupe on unique input does."""
    if not DEDUPE_ENABLED:
        return Result("dedupe", items=prev.items)
    return Result("dedupe", items=prev.items - 3)


DEDUPE_ENABLED = False


def index(prev: Result) -> Result:
    return Result("index", items=prev.items)


STAGES = [fetch, parse, enrich, dedupe, index]
MAX_RETRIES = 2
