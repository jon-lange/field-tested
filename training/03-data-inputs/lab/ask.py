#!/usr/bin/env python3
"""The pipeline.  python3 ask.py

Four questions. Four answers. Every one cites its sources, and one of them cites
three that agree.

Your job is to work out which answers are grounded in anything — without
changing the retriever or the corpus.
"""

from __future__ import annotations

import corpus


def main() -> int:
    print("build-cache assistant · retrieval-augmented\n")
    for question in corpus.QUESTIONS:
        context = corpus.retrieve(question)
        reply = corpus.answer(question, context)
        sources = sorted({name for name, _ in context})

        print(f"  Q  {question}")
        print(f"  A  {reply}")
        print(f"     sources: {', '.join(sources) if sources else '—'}"
              f"  ({len(context)} chunk(s))")
        print()

    print("  4 of 4 answered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
