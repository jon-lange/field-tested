#!/usr/bin/env python3
"""The prompt A/B.  python3 compare.py

v2 wins. Ship it?

Your job is to work out what the headline number is not telling you — without
changing either prompt or the eval set.
"""

from __future__ import annotations

import suite


def main() -> int:
    print("prompt evaluation · 200 cases\n")
    for v in ("v1", "v2"):
        print(f"  {v}  {suite.PROMPTS[v]}")
    print()

    a, b = suite.overall("v1"), suite.overall("v2")
    print(f"  v1 accuracy   {a:.1%}")
    print(f"  v2 accuracy   {b:.1%}")
    print(f"  delta         {b - a:+.1%}")
    print()
    print(f"  v2 wins on the eval set. Recommend rollout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
