#!/usr/bin/env python3
"""Three questions the pipeline does not ask.  python3 diagnose.py

Every figure is computed from the lab. Nothing is quoted.
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lab"))

import corpus  # noqa: E402


def stem(word: str) -> str:
    """Crude suffix stripping, and it earns its place.

    The first version compared raw words and reported the corpus had NO SOURCE
    for "triggers" — while the document said "triggered". A grounding check that
    flags a morphological variant as a missing fact is a check people learn to
    ignore, which is worse than not having one."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def terms(text: str) -> set[str]:
    return {stem(w) for w in re.findall(r"[a-z]{4,}", text.lower())}


def probe_corroboration() -> None:
    """Do the cited sources agree, or are they the same document?

    'Three sources agree' is the strongest signal a citation list can send, and
    it is worth nothing when the three are copies.
    """
    print("1. do the sources corroborate, or duplicate?")
    question = corpus.QUESTIONS[0]
    ctx = corpus.retrieve(question)
    print(f"   {question}")
    print(f"   cites {len({n for n, _ in ctx})} sources")

    worst = 0.0
    for i in range(len(ctx)):
        for j in range(i + 1, len(ctx)):
            r = difflib.SequenceMatcher(None, ctx[i][1], ctx[j][1]).ratio()
            worst = max(worst, r)
            print(f"     {ctx[i][0]:<34} vs {ctx[j][0]:<34} {r:.0%} identical")

    if worst > 0.70:
        print(f"   <-- up to {worst:.0%} identical. These are one runbook, pasted into")
        print("   three places. The answer has one source and three citations, and the")
        print("   citation count is the thing a reader trusts most.")
        print("   De-duplicate BEFORE counting sources, not after.")
    print()


def probe_truncation() -> None:
    """Does chunking cut anything mid-word?

    A boundary that lands inside a word lands inside a fact.
    """
    print("2. does chunking cut through the content?")
    broken = []
    for i, (name, chunk) in enumerate(corpus.CHUNKS):
        if len(chunk) == corpus.CHUNK_CHARS and not chunk[-1].isspace():
            nxt = corpus.CHUNKS[i + 1][1] if i + 1 < len(corpus.CHUNKS) else ""
            if nxt and not nxt[0].isspace() and nxt[0].isalpha():
                broken.append((name, chunk[-24:], nxt[:12]))

    print(f"   chunk size: {corpus.CHUNK_CHARS} characters, no overlap")
    print(f"   chunks total: {len(corpus.CHUNKS)}")
    for name, tail, head in broken:
        print(f"   <-- {name}")
        print(f"       ...{tail!r}  |  {head!r}...")
    if broken:
        print(f"   {len(broken)} boundary cuts a word in half. Neither chunk carries the")
        print("   whole sentence, so retrieval can match the topic and still hand the")
        print("   model a fact with its ending removed.")
        print("   Chunk on sentence boundaries, or overlap enough to survive one.")
    print()


def probe_grounding() -> None:
    """Is each answer supported by what was actually retrieved?

    The pipeline answers every question. That is not the same as every question
    having an answer in the corpus.
    """
    print("3. is every answer grounded in what was retrieved?")
    for question in corpus.QUESTIONS:
        ctx = corpus.retrieve(question)
        reply = corpus.answer(question, ctx)

        # Does the reply engage the question, or merely share its topic?
        # Stopwords stemmed too: "happens" becomes "happen", and an
        # unstemmed list stopped matching it the moment stemming was added.
        # Fixing one false positive introduced another.
        stop = {stem(w) for w in ("what", "when", "does", "happens", "long", "path")}
        q_terms = terms(question) - stop
        ctx_terms = terms(" ".join(c for _, c in ctx))
        missing = q_terms - ctx_terms
        # The sharper case: the corpus HAS the term and the answer skipped it.
        # Counting how many question terms the reply matched cannot see this —
        # a reply can match two and still ignore the one the question turns on.
        unused = (q_terms & ctx_terms) - terms(reply)

        flag = ""
        if missing:
            flag = f"NO SOURCE for {sorted(missing)}"
        elif unused:
            flag = (f"the context covers {sorted(unused)}, the answer does not "
                    "engage it")

        print(f"   {'!!' if flag else '  '} {question}")
        print(f"      -> {reply[:66]}")
        if flag:
            print(f"      <-- {flag}")
    print("   Nothing in the corpus mentions escalation, and the pipeline answered")
    print("   anyway — fluently, with a citation. A retriever that returns weak")
    print("   matches and a generator that never declines produce a confident")
    print("   answer to a question the corpus cannot support.")
    print("   Require a grounding score, and let the pipeline say it does not know.")
    print()


def main() -> int:
    print("diagnosing the pipeline — every figure computed from this lab\n")
    probe_corroboration()
    probe_truncation()
    probe_grounding()
    print("Four answers, four citations, and none of it evidence that the corpus")
    print("contained what was asked for.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
