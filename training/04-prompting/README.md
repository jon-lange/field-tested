---
proof: demo
title: Prompt engineering
dimension: 2
---

# 04 · Prompt engineering

> **Dimension 2 of 6.** Data inputs · **Prompt engineering** · Model selection ·
> Workflow architecture · Evaluation pipelines · Continuous monitoring

**Time:** about 45 minutes. **Prerequisites:** Python 3. No API key.

> **`proof: demo`** — a runnable demonstration, not a measurement. Every figure
> is computed from the lab. It makes no claim about how often this happens.

## The claim

> A prompt that scores higher is a fact about your eval set's weighting. It is
> not, on its own, evidence that it is better for anyone in particular.

```bash
cd lab && python3 compare.py
```

v2 beats v1 by **+4.9%** across 200 cases. Ship it?

## 1. An average improvement can contain a collapse

v2 improves `routine` by 8, `multiline` by 12, `truncated` by 8 — and drops
`non-english` from **80% to 10%**.

That class is 5% of the eval set, so a 70-point collapse costs the headline
**3.5%** against a **+4.9%** gain. The win is real. So is the regression. Only
one is in the summary.

The cause is in the prompt: v2 added *"Respond in English."* It did exactly what
it was told.

**Report per class, and gate on the worst one.**

## 2. An unbalanced eval set is an unratified weighting

`routine` has 120 cases; `non-english` has 10. Nobody chose that ratio — it is
whatever accumulated as failures were added and never rebalanced.

A single aggregate over it is a weighted score whose weights nobody signed off,
which is
[pattern 06](https://github.com/jon-lange/not-evidence/blob/main/patterns/06-refuse-unratified-weights.md)
arriving in a prompt A/B. That specimen measured **40.6% of defensible
weightings reversing a verdict**.

## 3. An instruction with no test is a preference

v2 also added *"Never include the raw log line."* No eval case fails if the model
ignores it — the accuracy number is identical either way. In the lab it is
violated on `truncated` inputs, and nothing notices.

**Add the negative case:** an input that would tempt the violation, asserted
against. Otherwise the instruction holds exactly as often as the model happens
to comply.

## What to take back

- [ ] Break your last prompt win down by input class. Look for a negative delta.
- [ ] Count cases per class in your eval set. Ask who ratified that ratio.
- [ ] List the instructions in your system prompt. For each, name the test that
      fails if it is ignored. Any without one are preferences.

**Previous:** [03 · Data inputs](../03-data-inputs/) · **Next:** [05 · Model selection](../05-model-selection/)
