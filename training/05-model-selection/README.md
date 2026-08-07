---
proof: demo
title: Model selection
dimension: 3
---

# 05 · Model selection

> **Dimension 3 of 6.** Data inputs · Prompt engineering · **Model selection** ·
> Workflow architecture · Evaluation pipelines · Continuous monitoring

**Time:** about 45 minutes. **Prerequisites:** Python 3. No API key.

> **`proof: demo`** — a runnable demonstration, not a measurement.

## The claim

> Two models with the same benchmark score are not interchangeable. The score is
> a mean, and means are where differences go to hide.

```bash
cd lab && python3 choose.py
```

Three candidates inside **0.7%** of each other. One is **10× cheaper**. The
decision looks like arithmetic.

## 1. A 0.7% spread can contain a 49-point one

Broken out by slice, `atlas-small` scores **41%** on billing tickets where the
others score 88–90%. Billing is 10% of volume, so the headline absorbs it and
three models share a number while behaving completely differently.

**Compare per slice.** A mean over slices is a claim about a weighting, and the
weighting came from whatever the benchmark happened to contain.

## 2. What was measured and never reported

`atlas-small` declines **14%** of tickets. Those are *correct refusals*, not
errors, so accuracy never moves — and every one is a ticket a human now handles.

Rank on tickets actually resolved rather than accuracy and the ordering changes.
That is
[pattern 07](https://github.com/jon-lange/not-evidence/blob/main/patterns/07-gate-over-refusal-separately.md):
quality without refusal beside it.

## 3. Cost per call is not cost per outcome

Per call: `$0.90` vs `$9.00`. Per resolved ticket the gap narrows — and the
14% going to a human queue costs a salary that appears on no table here.

The benchmark also never covered non-English tickets or anything over 4k tokens.
**No score is evidence about an uncovered case, in either direction.**

## What to take back

- [ ] Break your model comparison down by slice. Find the widest spread.
- [ ] Check whether refusal, truncation or format-compliance rates were measured
      and left out of the summary.
- [ ] Recompute cost per *resolved* unit, not per call.
- [ ] Write down what your benchmark does not cover, and stop treating its
      silence as a pass.

**Previous:** [04 · Prompt engineering](../04-prompting/) · **Next:** [06 · Workflow architecture](../06-workflow/)
