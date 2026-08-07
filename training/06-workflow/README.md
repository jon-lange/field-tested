---
proof: demo
title: Workflow architecture
dimension: 4
---

# 06 · Workflow architecture

> **Dimension 4 of 6.** Data inputs · Prompt engineering · Model selection ·
> **Workflow architecture** · Evaluation pipelines · Continuous monitoring

**Time:** about 45 minutes. **Prerequisites:** Python 3. No API key.

> **`proof: demo`** — a runnable demonstration, not a measurement.

## The claim

> A pipeline that reports success is telling you every stage returned. It is not
> telling you what any of them did.

```bash
cd lab && python3 run.py
```

Five stages, all `ok`, forty documents in and forty indexed.

## 1. The retry that worked is the one to worry about

`parse` raised `RuntimeError: malformed document at offset 12`, the runner
retried, the retry succeeded, and the line says `ok`.

Nothing counts how often a stage needs a retry. **A stage failing half the time
and a stage that has never failed produce the same output.** The retry count is
the earliest signal available and it is being discarded on every run.

## 2. A fallback that looks like the real path

The enrichment service was unreachable. The fallback returned the input
unenriched — a valid result, so the stage is `ok` and the pipeline is `SUCCESS`.

Forty documents were indexed. None were enriched. **A fallback indistinguishable
from the primary path converts an outage into a silent quality change**, and the
only place it appears is in whatever downstream consumer eventually notices the
data is thinner.

**Make degraded a third outcome, not a shade of success.**

## 3. The stage that did nothing

`dedupe` is behind a flag that defaults off. It returns success having done
nothing — which is byte-identical to a working dedupe over input that happened
to be unique. That is why nobody catches it.

It is in the architecture diagram. It is in the run log. It has never removed a
duplicate.

**Report what a stage did, not that it ran.** Items in, items out, work
performed.

## What to take back

- [ ] Find your most-retried stage. Is the retry count emitted anywhere?
- [ ] List every fallback. For each, name how a consumer could tell it fired.
- [ ] Find a stage behind a feature flag. Confirm it is on where you think.
- [ ] Change one stage's summary from "ran" to "did N units of work."

## Reading

- [Pattern 11 · Green Is Not Evidence](https://github.com/jon-lange/not-evidence/blob/main/patterns/11-green-is-not-evidence.md)
  — the same shape at the assertion level

**Previous:** [05 · Model selection](../05-model-selection/)
