## Precision@K (plain definition)

**Precision@K** answers:

> **“Out of the top K documents I retrieved, how many are actually relevant?”**

It measures **how noisy or clean** your retrieval results are.

---

## The formula (written clearly)

```
Precision@K =
(number of relevant documents retrieved in the top K results)
-------------------------------------------------------------
(K)
```

---

## Concrete example

For **one query**:

* Retriever returns **top 5 documents**
* **2 of them are relevant**
* **3 are irrelevant**

```
Precision@5 = 2 / 5 = 0.4
```

Meaning:

> 40% of what you retrieved is useful,
> 60% is noise.

---

## Edge cases

### All retrieved docs are relevant

```
Precision@K = K / K = 1.0
```

### None are relevant

```
Precision@K = 0 / K = 0.0
```

---

## Precision vs Recall (side-by-side)

| Metric      | Question it answers                                |
| ----------- | -------------------------------------------------- |
| Recall@K    | “Did I retrieve all relevant documents?”           |
| Precision@K | “How many of my retrieved documents are relevant?” |

They pull in **opposite directions**.

---

## Why Precision@K is *less important* in RAG

This is counter-intuitive but critical.

In RAG:

* ❌ Missing relevant info → **hallucinations**
* ✅ Extra irrelevant info → **can often be ignored**

So:

* **Recall > Precision** in early retrieval
* Precision becomes important **after reranking**

---

## Typical Precision@K behavior in RAG

### High Recall, Low Precision (very common)

* Vector search retrieves many semi-related chunks
* LLM still answers correctly (sometimes)
* Context window fills fast

### High Precision, Low Recall (dangerous)

* Retriever is “too strict”
* Important info is missing
* LLM confidently makes things up

---

## Precision@K improves *later* in the pipeline

Precision is usually improved by:

* Cross-encoder rerankers
* Metadata filtering
* Query rewriting
* Context window trimming

Not by embeddings alone.

---

## Typical Precision@K ranges

Very rough intuition:

* **< 0.2** → Very noisy
* **0.2 – 0.4** → Normal for raw vector search
* **0.4 – 0.6** → Good after reranking
* **0.6+** → Very clean retrieval

Don’t panic if raw precision is low.

---

## Precision@K + Recall@K together

You almost always look at them **together**:

| Scenario                    | Recall | Precision | Outcome               |
| --------------------------- | ------ | --------- | --------------------- |
| Low recall, high precision  | ❌      | ✅         | Hallucinations        |
| High recall, low precision  | ✅      | ❌         | Noisy but salvageable |
| High recall, high precision | ✅      | ✅         | Ideal                 |
| Low both                    | ❌      | ❌         | Broken retrieval      |

---

## One-sentence mental model

> **Precision@K measures how much junk you brought with you.**

Recall@K measures whether you brought the **right stuff at all**.

---

## Final RAG takeaway

**Retrieval tuning order:**

1. Fix **Recall@K**
2. Improve **MRR**
3. Clean up with **Precision@K**
4. Polish ranking with **nDCG**

