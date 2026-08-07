---
proof: measured
source: https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md
title: Continuous monitoring
dimension: 6
---

# 02 · Continuous monitoring

> **Dimension 6 of 6.** Data inputs · Prompt engineering · Model selection ·
> Workflow architecture · Evaluation pipelines · **Continuous monitoring**

[Module 01](../01-evaluation/) was about whether your tests mean anything. This
one is about whether your dashboard does — which fails differently, and worse,
because a dashboard is consulted during an incident rather than before a merge.

**Time:** about an hour. **Prerequisites:** Python 3. No API key, no network.

---

## The claim

> A green dashboard is a fact about your panels. It is not, on its own, evidence
> about the system.

Three ways that goes wrong, all of them ordinary:

| Failure | What you see | What is true |
|---|---|---|
| **The alert that cannot fire** | No alerts firing | The rule queries a metric nothing emits |
| **The average that hides a segment** | A healthy headline number | A small segment is failing constantly |
| **The metric on no panel** | Everything charted is flat | Something you do not chart moved 9× |

Each one produces a dashboard **indistinguishable from a healthy system.** That
is the whole difficulty: there is nothing to notice.

---

## Do the lab first

```bash
cd lab && python3 dashboard.py
```

Thirty days, three panels, three alerts, nothing firing. All three failures above
are present. [`lab/README.md`](lab/) has the brief.

---

## 1. An alert that has never fired proves nothing

Two systems produce an identical dashboard: one where the rule watches a healthy
service, and one where the rule queries a metric that no longer exists. A
refactor renames `summarizer.latency_p50` to `summariser.latency_p50_ms`, the
rule is not updated, the query returns no data — and **no data does not breach a
threshold.** The panel stays quiet forever.

This is [module 01's vacuous test](../01-evaluation/) wearing different clothes,
and it is worse here, because a test suite runs on every merge while an alert
rule is consulted only when something has already gone wrong.

**The technique is the same:** make it fire on purpose. Force the condition,
watch the alert go red, restore. An alert nobody has ever seen fire is not
monitoring — it is decoration with a threshold on it.

> **Evidence:** the technique this generalises is measured in
> [specimen 11](https://github.com/jon-lange/not-evidence/blob/main/specimens/11-mutation-check/RESULTS.md).
> Two of six variants passed while the property they guarded was broken, and the
> passing output was identical to the working case.

---

## 2. Alert on the worst segment, not the mean

The lab's overall success rate is **98.47%**, comfortably above its 98% threshold.
One segment — 3% of traffic — succeeds **70.83%** of the time. It moves the
headline by **0.87%**, which is inside the rounding of a green panel, and costs
about **35 failed requests a day** that nothing reports.

Smaller segments hide better. A tail worth 1% of traffic can fail outright and
never move a mean.

**Chart and alert per segment.** If you only have room for one number, use the
worst segment rather than the average — it is the one a customer is actually
experiencing.

> This is the failure the whole catalogue shares: *a comfortable summary is where
> the dangerous case hides, because averaging is how a failure stops looking
> like one.*

---

## 3. The metric on no panel

The lab charts quality, which sits at **4.60** for thirty days. It also emits
refusal rate, which goes from **2% to 18%** over the same window — a **9×**
increase, on no panel, under no alert.

Nothing broke. Quality is genuinely fine. The system is simply declining nine
times as much work as it used to, and every chart agrees that things are normal.

Folding refusal into a composite quality score does not help: the composite is
dominated by quality, so the number barely moves. **Keep two numbers and gate on
both.**

> **Evidence:** measured in
> [specimen 07](https://github.com/jon-lange/not-evidence/blob/main/specimens/07-over-refusal/RESULTS.md)
> across five models and two vendors. That run also contradicted the pattern it
> was built for — the "newer models refuse more" claim did not reproduce, and the
> entry now argues for measurement discipline rather than a trend.

---

## What to take back to your own dashboards

- [ ] Pick your most important alert. **Force it to fire.** If you cannot, or
      nothing happens, you have found something today.
- [ ] List every alert that has never fired. For each, decide whether that is
      health or silence — you cannot tell from the dashboard.
- [ ] Take your headline reliability number. Break it by segment. Look at the
      worst one.
- [ ] Name one thing your system does that no panel charts. Refusals, retries,
      truncations, fallbacks. Chart it.
- [ ] Check whether any composite is hiding a component that moved.

---

## Reading

- [not-evidence](https://github.com/jon-lange/not-evidence) — the catalogue, with
  [EVIDENCE.md](https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md)
  as the one-page record
- Patterns [11](https://github.com/jon-lange/not-evidence/blob/main/patterns/11-green-is-not-evidence.md),
  [07](https://github.com/jon-lange/not-evidence/blob/main/patterns/07-gate-over-refusal-separately.md),
  [08](https://github.com/jon-lange/not-evidence/blob/main/patterns/08-remembered-is-not-current.md)

**Previous:** [01 · Evaluation pipelines](../01-evaluation/)
