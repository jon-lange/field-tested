---
proof: demo
title: Data inputs
dimension: 1
---

# 03 · Data inputs

> **Dimension 1 of 6.** **Data inputs** · Prompt engineering · Model selection ·
> Workflow architecture · Evaluation pipelines · Continuous monitoring

Modules [01](../01-evaluation/) and [02](../02-monitoring/) were about whether
your checks are telling the truth. This one is earlier in the pipeline: whether
what reaches the model is what you think reaches it.

**Time:** about an hour. **Prerequisites:** Python 3. No API key, no network.

> **`proof: demo`** — this module ships a runnable demonstration, not a
> measurement. Every figure it prints is computed from the lab in front of you.
> Unlike 01 and 02 it makes no claim about how often these occur in the wild,
> because nothing here measured that.

---

## The claim

> A confident answer with three citations is a fact about your retriever. It is
> not, on its own, evidence that the corpus contained what you asked for.

| Failure | What you see | What is true |
|---|---|---|
| **Corroboration that isn't** | Three sources agree | One document, pasted three times |
| **The boundary in the middle of a fact** | A relevant chunk | The sentence was cut mid-word |
| **Answering from absence** | A fluent, cited answer | Nothing in the corpus addresses the question |

---

## Do the lab first

```bash
cd lab && python3 ask.py
```

Four questions, four answers, every one cited. [`lab/README.md`](lab/) has the
brief.

---

## 1. Count sources after de-duplication, not before

The lab's first answer cites three documents. They are **up to 91% identical** —
one runbook, copied into a second wiki space and an archive.

Citation count is the strongest trust signal a RAG answer sends, and it is the
easiest to inflate by accident. Nobody duplicated that runbook to game anything;
someone pasted it somewhere convenient, twice, over three years.

**De-duplicate before you count.** Near-duplicate detection on ingest, not a
distinct-filename check at display time — the filenames were all different.

---

## 2. A boundary that lands inside a word lands inside a fact

Fixed-width chunking with no overlap, at 180 characters. **Four boundaries in
this corpus cut a word in half:**

```
...'marked unhealthy and dr'  |  'ained.'...
```

Retrieval still matches the topic, and the model still receives a chunk that
looks complete. What it does not receive is the end of the sentence.

**Chunk on sentence boundaries, or overlap enough to survive one.** And check —
the count is one loop over your chunks.

---

## 3. Let the pipeline say it does not know

The corpus contains nothing about escalation paths. Asked for one, the pipeline
returned *"Retention is enforced by a nightly sweep"* — fluent, on-topic, cited,
and not an answer.

Two ordinary things combine: a retriever that returns its best match no matter
how weak, and a generator that never declines. Neither is broken. Together they
produce a confident answer to a question the corpus cannot support.

A subtler case in the same lab: asked what happens when an agent misses
heartbeats, the answer describes the heartbeat interval. The corpus **does**
cover it; the answer simply engages a different sentence. Counting how many
question terms the reply matched will not catch this — a reply can match two
terms and still skip the one the question turns on.

**Require a grounding threshold and allow refusal.** That is
[pattern 01](https://github.com/jon-lange/not-evidence/blob/main/patterns/01-grounded-or-refuse.md),
and its specimen is worth reading precisely because it *contradicted* the
prediction it was built to confirm.

---

## What to take back to your own pipeline

- [ ] Run near-duplicate detection over your corpus. Report the count.
- [ ] Count how many of your chunk boundaries land inside a word.
- [ ] Ask your system something your corpus definitely does not contain. See
      whether it declines.
- [ ] Take one answer and check every question term against the retrieved
      context, not against the answer.

---

## Reading

- [not-evidence](https://github.com/jon-lange/not-evidence) — the catalogue
- Patterns [01](https://github.com/jon-lange/not-evidence/blob/main/patterns/01-grounded-or-refuse.md),
  [12](https://github.com/jon-lange/not-evidence/blob/main/patterns/12-distrust-the-sanitization-label.md)

**Previous:** [02 · Continuous monitoring](../02-monitoring/)
