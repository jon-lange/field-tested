# Solution

```bash
python3 diagnose.py
```

Every figure it prints is computed from the lab. Nothing is quoted.

---

## Check 1 — the credential leak was vacuous

`SUMMARY_LOGGING_ENABLED = False` in `subject.py`, so `_log()` never appends.
The assertion `API_TOKEN not in s.logged()` is satisfied by an empty string.

**Redaction is implemented correctly.** That is what makes this the interesting
case rather than a bug hunt: nothing is broken, and the check is still not
evidence. A rollout flag defaulting off is not a defect — it is Tuesday.

`diagnose.py` no-ops `redact` and re-runs the check. It still passes. A check
that passes with the guarded behaviour destroyed was never watching it.

**The fix is not a better assertion.** It is a liveness proof next to the
existing one: *with redaction reduced to a no-op, this must fail.*

## Check 2 — the judge was saturated

`judge_quality` returns `5` for any input — a good summary, `"asdf"`, and the
empty string alike. The `>= 4` threshold cannot fail, so it cannot inform a
release.

A single score cannot show you this. A second, obviously-worse input can, and
costs one call.

## Check 3 — the winner was a property of the weights

`WEIGHTS` picks `candidate-a`. Nobody ratified them.

Sweeping the simplex on a grid: **20,794 of 53,130 weightings — 39.1% — pick
`candidate-b` instead.** The two candidates trade off genuinely; `a` wins on
latency and cost, `b` on coverage and safety. Which matters is a business
decision, and the scorecard silently made it.

Reporting "candidate-a wins" is reporting one weighting's opinion. Report the
share, or get the weights ratified by whoever owns the tradeoff.

---

## The shape all three share

Each check produced output **indistinguishable from a working check.** No error,
no warning, no anomaly. That is why none was caught by review: there was nothing
to see.

The generalisation:

> Given a green result, ask what a *broken* system would have printed. If the
> answer is "the same thing," the result is not evidence.

Every technique here is a way of manufacturing the failing case so you can
confirm the check distinguishes it.

---

## Extending the lab

- Flip `SUMMARY_LOGGING_ENABLED` to `True`. Check 1 becomes live — confirm that
  `diagnose.py` now reports it as such. **A diagnostic that cannot report "this
  one is fine" has the same problem as the checks it is auditing.**
- Make `judge_quality` return a length-based score. Watch check 2 gain signal.
- Change one candidate's scores so the flip share goes to zero, and confirm the
  sweep agrees. A verdict robust across the whole simplex is one you can report
  as a winner.
