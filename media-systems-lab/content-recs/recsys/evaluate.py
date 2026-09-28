from __future__ import annotations

import math

from .engine import HybridRecommender
from .models import ContentItem, WatchEvent


def evaluate_leave_one_out(catalog: list[ContentItem], events: list[WatchEvent], k: int = 5) -> dict[str, float]:
    by_user: dict[str, list[WatchEvent]] = {}
    for event in events:
        by_user.setdefault(event.user_id, []).append(event)

    train: list[WatchEvent] = []
    held_out: dict[str, WatchEvent] = {}
    for user, rows in by_user.items():
        ordered = sorted(rows, key=lambda e: e.days_ago, reverse=True)  # oldest -> newest
        if len(ordered) < 2:
            train.extend(ordered)
            continue
        train.extend(ordered[:-1])
        held_out[user] = ordered[-1]

    engine = HybridRecommender(catalog, train)
    recalls: list[float] = []
    ndcgs: list[float] = []
    recommended_ids: set[str] = set()

    for user, target in held_out.items():
        recs = engine.recommend(user, k=k)
        ids = [r.content_id for r in recs]
        recommended_ids.update(ids)
        if target.content_id in ids:
            rank = ids.index(target.content_id) + 1
            recalls.append(1.0)
            ndcgs.append(1.0 / math.log2(rank + 1))
        else:
            recalls.append(0.0)
            ndcgs.append(0.0)

    catalog_size = max(1, len(catalog))
    return {
        f"recall@{k}": round(sum(recalls) / len(recalls), 4) if recalls else 0.0,
        f"ndcg@{k}": round(sum(ndcgs) / len(ndcgs), 4) if ndcgs else 0.0,
        "catalog_coverage": round(len(recommended_ids) / catalog_size, 4),
        "evaluated_users": float(len(recalls)),
    }
