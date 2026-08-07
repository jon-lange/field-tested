# Solution

```bash
python3 diagnose.py
```

## 1. Three citations, one document

`runbook-cache-evictions`, `-copy` and `-archive` are **76–91% identical**. The
filenames differ, so a distinct-source count sees three.

**De-duplicate on ingest.** A similarity check over the corpus is a few lines,
and it is the difference between "three sources agree" meaning something and
meaning nothing.

## 2. Four chunk boundaries cut a word in half

180 characters, no overlap:

```
...'marked unhealthy and dr'  |  'ained.'...
```

The chunk still retrieves. It just no longer ends where the fact ends.

## 3. Two different grounding failures

**Answering from absence.** Nothing in the corpus mentions escalation. The
pipeline answered anyway, because the retriever returns its best match however
weak and the generator never declines.

**Engaging the wrong sentence.** Asked what happens when an agent *misses*
heartbeats, the answer gives the heartbeat interval. The corpus covers the real
answer — the reply just does not use it.

The second is why the check compares question terms against **the retrieved
context** and then against **the reply**, rather than counting matches. A reply
can match two question terms and still skip the one that matters.

---

## Two false positives found while building this

Worth recording, because both are the failure mode the catalogue is about,
appearing in the diagnostic rather than the thing being diagnosed.

**"NO SOURCE for `triggers`"** — the corpus said *triggered*. A grounding check
that flags a morphological variant as a missing fact is a check people learn to
ignore. Fixed with crude stemming.

**"NO SOURCE for `happen`"** — fixing the first broke the second. The stopword
list still held `happens`, which no longer matched once terms were stemmed. The
stopwords had to be stemmed too.

A diagnostic that cries wolf is worse than none, and both of these would have.

---

## The shape all three share

Every answer was fluent, cited, and on-topic. **None of that is evidence the
corpus contained what was asked for.**

> Given a confident answer, ask what the pipeline would have returned if the
> corpus were empty. If the answer is "something that looks like this," the
> citation is decoration.

## Extending the lab

- Set `CHUNK_CHARS` to a value that splits no words. Confirm the truncation
  count goes to zero — **a diagnostic that cannot report "this one is fine" has
  the same problem as the pipeline it audits.**
- Delete the two duplicate runbooks and watch the corroboration finding vanish.
- Add an escalation runbook and confirm the last question stops flagging.
