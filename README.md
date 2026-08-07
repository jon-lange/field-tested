# field-tested

Building blocks for production AI, where every block says how you know it works.

There is no shortage of collections of agents, prompts, and skills. What is
scarce is any of them telling you whether anyone checked. **Every block here
declares its own evidence, in frontmatter, and a script enforces that it does.**

```yaml
proof: measured    # a figure, and the specimen that produced it
proof: tested      # a runnable test in this repository
proof: demo        # a runnable demonstration
proof: unproven    # declared as such, with what would prove it
```

`unproven` is the load-bearing one. You may publish something you have not
validated. You may not publish it looking validated.

---

## What is here

| | |
|---|---|
| [`training/01-evaluation`](training/01-evaluation/) | **How to tell whether your eval suite is telling you the truth.** A release gate with three green checks, all of them lying. About an hour, no API key. |

More as it is built. This repository grows; the quality floor does not move.

---

## Why these blocks and not others

The through-line is a framework I use to separate production AI from an
impressive demo — six dimensions, of which two currently have published evidence
behind them:

| | Dimension | Evidence |
|---|---|---|
| 1 | Data inputs | — |
| 2 | Prompt engineering | — |
| 3 | Model selection | — |
| 4 | Workflow architecture | — |
| 5 | **Evaluation pipelines** | [not-evidence](https://github.com/jon-lange/not-evidence) — 12 specimens |
| 6 | **Continuous monitoring** | partial |

The empty rows are the roadmap. A block arrives when there is something true to
say about it, not when the grid looks incomplete.

---

## The bound, and why this repository does not have one

[not-evidence](https://github.com/jon-lange/not-evidence) is bounded: twelve
entries, then finished. That bound is the most useful thing about it, and it is
why it can be cited.

This repository cannot be bounded — growing is the point. So it needs the other
mechanism: not a limit on how much, but a floor on what counts, checked rather
than promised. That is the `proof:` contract above.

An open-ended collection with no floor is how a catalogue becomes a junk drawer.

---

## Evidence

Where a block says `proof: measured`, the figure comes from a specimen in
[not-evidence](https://github.com/jon-lange/not-evidence) that ships the harness
that produced it. Ten of those twelve entries were revised because their own
measurements contradicted them; five had their central claim fail.

Nothing here quotes a number it did not generate.

## Licence

Apache 2.0. Take it.
