# Lab — the gate that shouldn't have opened

You have inherited a release gate for a docs-summarisation feature. Three checks:
a credential-leak check, a model-judged quality threshold, and a weighted
scorecard that picks which configuration ships.

```bash
python3 gate.py
```

All three pass. The feature is cleared to ship.

## Your task

**Do not change what the checks assert.** Every assertion in `gate.py` is
reasonable and states something you genuinely want to be true.

For each of the three, answer one question:

> **If the thing this check exists to catch were happening right now, would this
> check tell me?**

Write down how you would find out. Then find out.

## Rules

- Standard library only. No network, no keys, no cost.
- You may add files. You may not weaken an existing assertion to make a point.
- `subject.py` is the system under test. Reading it will give away part of the
  answer — try the question above first.

## Hints, if you want them

<details>
<summary>Check 1 — the credential leak</summary>

A test that passes proves the assertion held. It does not prove the assertion
was *watching* anything. How would you tell those two apart?

Try breaking the behaviour the check is supposed to be guarding, and running the
check again.
</details>

<details>
<summary>Check 2 — the quality judge</summary>

You have one score, from one input. What would you learn from a second input
that is obviously worse?
</details>

<details>
<summary>Check 3 — the scorecard</summary>

Where did the weights come from? Who ratified them? If a colleague argued for a
different but equally defensible weighting, would the winner change — and how
much of the space of defensible weightings would you have to try before you knew?
</details>

## When you are done

```bash
python3 ../solution/diagnose.py
```

It computes every figure it prints from this lab. Compare it against what you
found.
