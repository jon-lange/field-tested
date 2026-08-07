#!/usr/bin/env python3
"""Enforce the proof contract.  python3 scripts/check.py

Every block declares how you know it works. Four values, and one of them is an
admission:

    measured   a figure, and the specimen that produced it
    tested     a runnable test in this repository
    demo       a runnable demonstration
    unproven   declared as such, and says what would prove it

`unproven` is why the contract works at all. A rule that only permitted validated
things would be ignored the first time something useful was not, and then the
frontmatter would mean nothing. Permitting it, and requiring it to be *said*, is
the difference between a floor and a wish.

The checks:

  - every block has a README.md with frontmatter
  - `proof` is present and in the vocabulary
  - `measured` cites a source; `unproven` says what would prove it
  - anything a block claims to run, runs
  - README.md lists every block, so none is published unlisted

Standard library only. Exit 0 clean, 1 on any failure.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROOF = {"measured", "tested", "demo", "unproven"}

# Derived from the interpreter rather than typed, so it cannot go stale against
# the Python a reader actually has. Falls back to a hand list on interpreters
# that do not expose it.
try:
    STDLIB = set(sys.stdlib_module_names)  # 3.10+
except AttributeError:  # pragma: no cover
    STDLIB = {"__future__", "sys", "os", "re", "json", "pathlib", "subprocess",
              "itertools", "dataclasses", "contextlib", "typing", "collections",
              "math", "textwrap", "argparse", "wave", "html"}


def frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    try:
        _, block, _ = text.split("---", 2)
    except ValueError:
        return {}
    meta = {}
    for line in block.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.split("#")[0].strip().strip('"')
    return meta


def blocks() -> list[Path]:
    """A block is any directory holding a README.md, one level under a category
    directory. Discovered rather than listed, so a block cannot be added without
    the contract seeing it."""
    found = []
    for category in sorted(p for p in ROOT.iterdir()
                           if p.is_dir() and not p.name.startswith((".", "_"))
                           and p.name != "scripts"):
        found += [d for d in sorted(category.iterdir())
                  if d.is_dir() and (d / "README.md").is_file()]
    return found


def main() -> int:
    problems: list[str] = []
    checked = 0
    index = (ROOT / "README.md").read_text()

    found = blocks()
    if not found:
        print("BLOCKED - no blocks found. A clean result from here would mean "
              "nothing, which is the failure this contract is about.")
        return 1

    for block in found:
        rel = block.relative_to(ROOT).as_posix()
        meta = frontmatter((block / "README.md").read_text())
        checked += 1

        proof = meta.get("proof", "")
        if not proof:
            problems.append(f"{rel}: no `proof:` in frontmatter")
            continue
        if proof not in PROOF:
            problems.append(
                f"{rel}: proof {proof!r} is outside the vocabulary "
                f"({', '.join(sorted(PROOF))})")
            continue

        # An admission has to admit something specific.
        if proof == "unproven" and not meta.get("would_prove"):
            problems.append(
                f"{rel}: proof: unproven without `would_prove:` — an admission "
                "that does not say what would settle it is not an admission")
        if proof == "measured" and not meta.get("source"):
            problems.append(
                f"{rel}: proof: measured without `source:` — a figure with no "
                "working is an assertion")

        # Anything a block tells you to run has to exist.
        #
        # Found by mutation: the first version of this anchored on ^\s*python3,
        # which never matched, because the commands people actually write are
        # `cd lab && python3 gate.py`. It checked nothing and reported clean —
        # a rule shaped exactly like the failure this repository teaches.
        #
        # Scoped to a claim that is true: every script a block names must exist
        # somewhere inside that block. It does not model the reader's working
        # directory, and does not pretend to.
        present = {p.name for p in block.rglob("*.py")}
        for doc in block.rglob("*.md"):
            for script in re.findall(r"python3 ([\w./-]+\.py)", doc.read_text()):
                if Path(script).name not in present:
                    problems.append(
                        f"{rel}: {doc.relative_to(block).as_posix()} says to run "
                        f"`python3 {script}`, which is not in this block")

        if rel not in index:
            problems.append(f"{rel}: not listed in README.md — published and unfindable")

        # Every block promises it runs with nothing installed. A stray import
        # makes that false for a reader on a clean machine, and it is the only
        # promise these modules make about running at all.
        #
        # Local modules are not dependencies: the labs import their own
        # `subject`, `gate`, `telemetry`. A first pass flagged all of those and
        # would have taught its author to ignore it, which is how a rule that
        # fires on innocent input stops being a rule.
        local = {p.stem for p in block.rglob("*.py")}
        for src in sorted(block.rglob("*.py")):
            for line in src.read_text().splitlines():
                m = re.match(r"\s*(?:from|import)\s+([\w.]+)", line)
                if not m:
                    continue
                top = m.group(1).split(".")[0]
                if top in local or top in STDLIB:
                    continue
                problems.append(
                    f"{rel}: {src.relative_to(block).as_posix()} imports {top!r}, "
                    "which is neither standard library nor part of this block")

    print(f"  checked {checked} block(s)")
    if problems:
        print(f"\nBLOCKED - {len(problems)} problem(s)\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print("  every block declares how you know it works")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
