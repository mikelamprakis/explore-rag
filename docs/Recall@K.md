# 1️⃣ What Recall@K means

**Recall@K** measures **coverage**.

> It answers:
> **“Did the retriever manage to fetch *all the relevant documents* within the top K results?”**

It does **not care about ranking order**, only whether relevant items appear *anywhere* in the top K.

---

# 2️⃣ Formal definition

For a single query:

```
Recall@K =
(number of relevant documents retrieved in the top K results)
----------------------------------------------------------------
(total number of relevant documents for that query)

```

Overall Recall@K is the **average across queries**.

---

# 3️⃣ Simple RAG example

Assume for a query there are **4 relevant chunks** in the corpus.

### Retrieved top-5 chunks:

* 2 are relevant
* 3 are irrelevant

![img_6.png](img/img_6.png)

If all 4 relevant chunks appear somewhere in top-5:

![img_7.png](img/img_7.png)

---

# 4️⃣ Why Recall@K is critical in RAG

RAG systems **cannot generate correct answers** if the required information is **never retrieved**.

Recall@K answers:

> **“Did we even give the LLM a chance?”**

Low recall means:

* Hallucination is guaranteed
* Prompt tuning won’t help
* Model size doesn’t matter

---

# 5️⃣ Recall@K ignores rank — on purpose

This is intentional.

| Metric   | Cares about rank? |
| -------- | ----------------- |
| MRR      | ✅ Very much       |
| nDCG     | ✅ Gradually       |
| Recall@K | ❌ Not at all      |

You can retrieve relevant chunks at ranks **2, 5, and 9**, and Recall@10 will still be **1.0**.

---

# 6️⃣ Typical K values in RAG

Common choices:

| K         | Use case              |
| --------- | --------------------- |
| Recall@3  | Tight context windows |
| Recall@5  | Standard QA           |
| Recall@10 | Long-context models   |
| Recall@20 | Multi-hop reasoning   |

**Choose K to match your context budget**, not arbitrarily.

---

# 7️⃣ Binary vs multi-relevance recall

### Binary Recall (most common)

* Relevant = yes/no
* Simple and fast

### Graded Recall (less common)

* Count only relevance ≥ threshold
* Useful when labeling is nuanced

In RAG, **binary recall** is usually enough.

---

# 8️⃣ Common Recall@K failure modes

### ❌ Low Recall

* Poor embeddings for domain
* Overly aggressive chunking
* Queries are underspecified
* Vector-only search (no BM25)
* Index filtering mistakes

### ❌ High Recall but bad answers

* Too many irrelevant chunks
* No reranking
* Context truncation
* Prompt ignores lower-ranked docs

---

# 9️⃣ Recall@K vs Precision@K (important contrast)

| Metric      | Focus                          |
| ----------- | ------------------------------ |
| Recall@K    | “Did I get *everything*?”      |
| Precision@K | “Did I get *only good stuff*?” |

In RAG:

* **Recall > Precision**
* Noise can be filtered
* Missing info cannot be recovered

---

# 🔟 How Recall@K fits with MRR and nDCG

Think of retrieval quality as **three gates**:

1️⃣ **Recall@K** – Did we retrieve the needed info at all?
2️⃣ **MRR** – Did we retrieve it early enough?
3️⃣ **nDCG** – Did we order all useful info well?

| Scenario              | Recall | MRR | nDCG | Outcome        |
| --------------------- | ------ | --- | ---- | -------------- |
| Low recall            | ❌      | ❌   | ❌    | Hallucinations |
| High recall, low MRR  | ✅      | ❌   | ⚠️   | Weak answers   |
| High recall, high MRR | ✅      | ✅   | ⚠️   | OK answers     |
| All high              | ✅      | ✅   | ✅    | Strong RAG     |

---

# 1️⃣1️⃣ Typical target ranges (rough)

For production RAG:

* **Recall@5 ≥ 0.8**
* **Recall@10 ≥ 0.9**

If Recall@K is low:

> Stop tuning the LLM — fix retrieval.

---

# 🔑 Final mental model

Think of Recall@K as:

> **“Did I bring the right books into the room?”**

MRR asks:

> “Is the right book already open on the desk?”

nDCG asks:

> “Are the books arranged in a useful order?”

