---
proof: measured
source: https://github.com/jon-lange/not-evidence/blob/main/EVIDENCE.md
title: Evaluation pipelines
dimension: 5
---

# 01 · Evaluation pipelines

> **Dimension 5 of 6.** Data inputs · Prompt engineering · Model selection ·
> Workflow architecture · **Evaluation pipelines** · Continuous monitoring

Most material on evals teaches you how to build one. This teaches you how to
tell whether the one you built is telling you the truth — which is a different
skill, and the one that decides whether a release gate means anything.

**Time:** about an hour. **Prerequisites:** Python 3. No API key, no network,
no cost.

---

## The claim

> A green evaluation suite is a fact about the run. It is not, on its own,
> evidence about the system.

Three ways that goes wrong, each of them ordinary, each of them silent:

| Failure | What you see | What is true |
|---|---|---|
| **The vacuous check** | A passing assertion | The assertion never observed the thing it names |
| **The saturated judge** | A high score | The judge returns that score for everything |
| **The unratified weighting** | A clear winner | A different defensible weighting picks the other one |

None announces itself. In all three cases the output is indistinguishable from
the output of a check that is working.

---

## Do the lab first

```bash
cd lab && python3 gate.py
```

Three checks, all green, feature cleared to ship. All three are lying, in the
three ways above. [`lab/README.md`](lab/) has the brief.

Work it before reading on — the lesson lands differently once you have watched
a check you believed go from `PASS` to `PASS` with the guarded behaviour
switched off.

---

## 1. A passing test is not a live test

An **absence assertion** — *the secret must not appear in the log* — is the most
common shape in safety-adjacent test suites, and the most likely to be vacuous.
It passes when the property holds. It also passes when nothing was logged at
all, when a rollout flag defaulted off, when a schema change stopped carrying
the field, and when the code path was never reached.

The property is intact in every one of those cases. What has been destroyed is
the **evidence**, and no amount of staring at a green tick will show you which
you have.

**The technique:** break what the assertion claims to guard, and require the
assertion to fail. If it still passes, it was never watching.

```python
require_live(logger, "redact", lambda event: event, absence_check)
```

*With redaction reduced to a no-op, this test must fail.* One line, next to the
assertion it is about, running every time — not a quarterly audit.

> **Evidence:** across one repository's twelve specimen suites, this technique
> found a defect in seven of them. One suite was mutation-checked and found to
> contain a test passing for the wrong reason *inside the specimen written to
> demonstrate the problem.*

---

## 2. Check that your judge discriminates before you trust its verdict

Model-as-judge is now standard, and the standard failure is not bias — it is
**saturation**. On a task set where both candidates are competent, a judge
returns 5/5 for everything. Every threshold passes. Nothing has been measured.

The second failure is **position instability**: the same judge, given the same
pair in the opposite order, picks the other one.

Both are cheap to detect and almost never checked:

- **Discrimination** — score something obviously poor. If it scores the same as
  something good, you have no signal.
- **Order stability** — run every pairwise comparison in both orders. Count
  the flips.

Do these *before* the verdict gates anything, because afterwards you cannot
distinguish "they were equal" from "the judge cannot tell them apart."

> **Evidence:** in a run of three judges over twelve items, two produced no
> signal at all and a third flipped on 6 of 12 comparisons **by position
> alone**. The same run set out to measure whether a judge favours its own model
> family, and found no such effect — the disqualifying problems were saturation
> and instability, neither of which is about lineage.

---

## 3. A weighted score is a claim about the weights

The moment you combine dimensions into one number, the verdict belongs to the
weighting as much as to the candidates. And the weighting is almost always
something somebody picked in a planning meeting and nobody has revisited.

Ask two questions before a composite gates a release:

1. **Who ratified these weights?** If the answer is nobody, the score is not a
   measurement, it is a preference with a decimal point.
2. **What share of defensible weightings picks the other candidate?** That is
   computable — sweep the simplex and count.

If a meaningful share reverses the verdict, **report the share, not the winner.**
That is an honest statement about a genuine tradeoff, and it hands the decision
to whoever actually owns it.

> **Evidence:** the lab computes this on its own scorecard and gets **39.1%
> across 53,130 weightings** — a decision that reverses under four in ten
> defensible weightings, reported as a clean win.

---

## 4. Measure refusal separately from quality

A composite quality score with refusals folded in is dominated by quality. Ship
a guardrail change and the quality number barely moves while the system quietly
starts declining work it used to do — and the dashboard stays green.

Keep two numbers. Gate on both.

---

## What to take back to your own suite

- [ ] Pick your most safety-relevant absence assertion. Break what it guards.
      Watch it fail. If it does not, you have found something today.
- [ ] Score one obviously-poor output with your judge. If it matches a good one,
      your judge is not measuring.
- [ ] Run one pairwise comparison in both orders. Count flips.
- [ ] Find your most consequential weighted score. Ask who ratified the weights.
- [ ] Check whether anything at all tracks refusal rate beside quality.

Each is minutes. Each has, somewhere, been the difference between a green suite
and a true one.

---

## Reading

The evidence cited above is measured, published, and reproducible — every figure
generated by the harness that ships with it:

- [not-evidence](https://github.com/langej117/not-evidence) — the catalogue, with
  [EVIDENCE.md](https://github.com/langej117/not-evidence/blob/main/EVIDENCE.md)
  as the one-page record
- [`tools/mutcheck.py`](https://github.com/langej117/not-evidence/blob/main/tools/mutcheck.py)
  — the liveness check from section 1, one file, no dependencies
- Patterns [11](https://github.com/langej117/not-evidence/blob/main/patterns/11-green-is-not-evidence.md),
  [05](https://github.com/langej117/not-evidence/blob/main/patterns/05-judge-cannot-share-a-family.md),
  [06](https://github.com/langej117/not-evidence/blob/main/patterns/06-refuse-unratified-weights.md),
  [07](https://github.com/langej117/not-evidence/blob/main/patterns/07-gate-over-refusal-separately.md)

Each entry states what would falsify it. Ten of the twelve were revised because
their own evidence contradicted them.

**Next:** 02 · Continuous monitoring — *the other dimension with measured
evidence behind it.*
