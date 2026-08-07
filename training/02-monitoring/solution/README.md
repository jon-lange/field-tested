# Solution

```bash
python3 diagnose.py
```

Every figure is computed from the lab.

## 1. One alert of three could never fire

`latency p50 above 3s` queries `summarizer.latency_p50`. The emitter writes
`summariser.latency_p50_ms` — renamed by a refactor, spelled differently, with a
unit suffix. The query returns no data, and **no data does not breach a
threshold.**

The rule has never fired. It never will. On the dashboard that is identical to a
service that has never been slow.

**The fix is not a better rule.** It is firing every rule on purpose at least
once and watching it go red. Same technique as module 01, aimed at alerts.

## 2. The average describes nobody

| segment | share | success |
|---|---|---|
| short | 74% | 99.49% |
| medium | 23% | 98.80% |
| **long** | **3%** | **70.83%** |

Overall: **98.47%**, against a 98% threshold. The failing segment moves the
headline by **0.87%** — inside the rounding of a green panel — and accounts for
roughly **35 failed requests a day**.

Nothing degraded. `long` was always this bad, which is why nobody noticed it
start. **Alert per segment, or on the worst one.**

## 3. Refusal rate went up 9× on no panel

Quality is charted and flat at **4.60** for thirty days. Refusal rate goes
**2% → 18%** over the same window and appears on no panel and in no alert.

Nothing is broken. Quality is genuinely fine. The system is declining nine times
as much work as it was, and every chart says normal.

A composite would not have caught it either: fold refusal into quality and the
composite is dominated by quality. **Two numbers, gated separately.**

---

## The shape all three share

Each produced a dashboard **indistinguishable from a healthy system.** No error,
no gap, no anomaly. Nothing to notice, which is why noticing is not the strategy.

> Given a green dashboard, ask what a *failing* system would have displayed. If
> the answer is "the same thing," the dashboard is not evidence.

## Extending the lab

- Fix the metric name in the dead alert. Confirm `diagnose.py` now reports it
  live — **a diagnostic that cannot say "this one is fine" has the same problem
  as the alerts it audits.**
- Add a per-segment alert and watch it fire on `long` while the overall panel
  stays green.
- Set every segment's success rate equal and confirm the aggregation finding
  disappears. A headline number is trustworthy exactly when the segments agree.
