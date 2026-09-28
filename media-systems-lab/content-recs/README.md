# Content Recommender

**A two-stage recommendation system for a streaming catalog: candidate generation first, ranking and diversity second.**

The project uses synthetic viewing histories so the entire pipeline is inspectable and reproducible.

## Architecture

```mermaid
flowchart LR
    E[Watch events] --> C1[Collaborative co-watch candidates]
    E --> C2[Content-profile candidates]
    E --> C3[Popularity / cold-start candidates]
    C1 --> R[Hybrid ranker]
    C2 --> R
    C3 --> R
    R --> D[MMR diversity reranker]
    D --> O[Top-K recommendations + explanations]
    O --> M[Recall@K / NDCG@K / catalog coverage]
```

## Candidate generation

`recsys/engine.py` builds three signals:

1. **Content affinity** — a recency- and completion-weighted viewer profile over genres/tags.
2. **Collaborative co-watch** — item-item similarity from shared viewer sets using Jaccard similarity.
3. **Popularity prior** — unique-viewer popularity, log-scaled so blockbusters help without dominating.

Seen titles are filtered before ranking.

## Ranking

The default hybrid score is:

```text
0.50 × content_affinity
+ 0.35 × collaborative_signal
+ 0.15 × popularity_prior
```

The top candidate pool is then reranked with **Maximal Marginal Relevance (MMR)** to trade a small amount of raw relevance for catalog diversity.

Each recommendation carries an explanation containing its strongest matched genres/tags and component scores.

## Cold start

With no watch history, the engine falls back to popularity while still applying the diversity reranker. The public API is the same for warm and cold users.

## Offline evaluation

`recsys/evaluate.py` performs leave-one-out evaluation and reports:

- **Recall@K**;
- **NDCG@K**;
- **catalog coverage**.

This makes recommendation quality a measurable contract instead of a hard-coded carousel.

## Run

```bash
cd content-recs
python demo.py
python -m unittest discover -s tests -v
```

## Production extensions

A production stack could replace the local candidate generators with ANN retrieval over learned embeddings, add contextual features and real-time session signals, train ranking models on implicit feedback, and evaluate online with watch-time, completion, retention, and experimentation guardrails.
