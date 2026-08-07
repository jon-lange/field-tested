# Lab — four answers, four citations

You have inherited a retrieval-augmented assistant over a small documentation
corpus.

```bash
python3 ask.py
```

Four questions. Four answers. Every one cites its sources, and the first cites
three that agree.

## Your task

**Do not change the retriever, the corpus, or the chunk size.**

For each answer, ask:

> **What would this pipeline have returned if the corpus did not contain the
> answer?**

Three of the four have something wrong with them. Find all three.

## Rules

- Standard library only. No network, no keys, no model.
- Deterministic — two runs produce identical output.
- `corpus.py` holds the documents, the chunker, the retriever and the stubbed
  generator. Reading it gives away the answers; try the question above first.

## Hints, if you want them

<details>
<summary>The first answer cites three sources</summary>

Open them. Are they three documents, or one document in three places? What would
you have to compare to tell, given the filenames are all different?
</details>

<details>
<summary>The chunker</summary>

Fixed width, no overlap. What happens to a sentence that straddles a boundary?
Print the chunks and look at where they end.
</details>

<details>
<summary>The last question</summary>

Does the corpus contain anything about escalation paths? What did the pipeline
do about that?

Then look again at the heartbeat answer. The corpus does cover it — so why is
that answer still wrong?
</details>

## When you are done

```bash
python3 ../solution/diagnose.py
```

Every figure is computed from this lab.
