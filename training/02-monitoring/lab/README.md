# Lab — the dashboard that was always going to be green

You have inherited a monitoring setup for a docs-summarisation service. Three
panels, three alert rules, thirty days of data.

```bash
python3 dashboard.py
```

Everything is green. No alerts are firing.

## Your task

**Do not change a threshold and do not relax a rule.** Every threshold here is
reasonable and every panel charts something worth charting.

For each of the three panels and each of the three alerts, answer one question:

> **If the thing this is supposed to catch were happening right now, would this
> tell me?**

There are three separate failures. Write down how you would find each one, then
find them.

## Rules

- Standard library only. No network, no keys, no cost.
- The data is deterministic — two runs produce identical numbers.
- `telemetry.py` is the system under observation. Reading it gives away the
  answers; try the question above first.

## Hints, if you want them

<details>
<summary>The alerts</summary>

Two systems produce an identical dashboard: one where a rule watches a healthy
service, and one where the rule watches nothing at all. How would you tell them
apart, without waiting for an incident?

What does a query return when the metric it names does not exist? Does that
breach a threshold?
</details>

<details>
<summary>The success rate</summary>

The number on the panel is a single figure for all traffic. Is every request the
same kind of request?

How much would a small, badly-failing slice move a mean?
</details>

<details>
<summary>What is not on the dashboard</summary>

Every panel is flat. That is consistent with a system where nothing is changing —
and also with a system where the thing that changed is not charted.

The service emits more metrics than it charts. Which ones, and what have they
been doing?
</details>

## When you are done

```bash
python3 ../solution/diagnose.py
```

Every figure it prints is computed from this lab. Compare it against what you
found.
