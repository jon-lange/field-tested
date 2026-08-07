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
| [`training/02-monitoring`](training/02-monitoring/) | **How to tell whether your dashboard is telling you the truth.** Three panels, three alerts, nothing firing — and an alert that never can. About an hour, no API key. |
| [`training/03-data-inputs`](training/03-data-inputs/) | **How to tell whether what reaches the model is what you think.** Four cited answers, three of them wrong — including one citing three sources that are one document. About an hour, no API key. |
| [`training/04-prompting`](training/04-prompting/) | **How to tell whether your prompt really improved.** v2 beats v1 by 4.9% and collapses one input class from 80% to 10%. About 45 minutes, no API key. |
| [`training/05-model-selection`](training/05-model-selection/) | **How to tell whether two models are interchangeable.** Three candidates inside 0.7%, one scoring 41% where the others score 90%. About 45 minutes, no API key. |
| [`training/06-workflow`](training/06-workflow/) | **How to tell what your pipeline actually did.** Five stages, all green — one failed and retried, one fell back silently, one did nothing. About 45 minutes, no API key. |

More as it is built. This repository grows; the quality floor does not move.

---

## Why these blocks and not others

The through-line is a framework I use to separate production AI from an
impressive demo — six dimensions, of which two currently have published evidence
behind them:

| | Dimension | Evidence |
|---|---|---|
| 1 | Data inputs | [module 03](training/03-data-inputs/) — demonstrated |
| 2 | Prompt engineering | [module 04](training/04-prompting/) — demonstrated |
| 3 | Model selection | [module 05](training/05-model-selection/) — demonstrated |
| 4 | Workflow architecture | [module 06](training/06-workflow/) — demonstrated |
| 5 | **Evaluation pipelines** | [not-evidence](https://github.com/jon-lange/not-evidence) — 12 specimens |
| 6 | **Continuous monitoring** | [not-evidence](https://github.com/jon-lange/not-evidence) — patterns 07, 11 |

All six now carry a block. Two are **measured** — a specimen produced the figure
and ships the harness. Four are **demonstrated**: the failure is real and
runnable, but nothing here measured how often it occurs, and the frontmatter
says so rather than letting the grid imply otherwise.

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
