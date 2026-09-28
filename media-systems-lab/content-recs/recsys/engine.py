from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass

from .models import ContentItem, WatchEvent


@dataclass(frozen=True)
class Recommendation:
    content_id: str
    title: str
    score: float
    content_score: float
    collaborative_score: float
    popularity_score: float
    explanation: str


class HybridRecommender:
    def __init__(self, catalog: list[ContentItem], events: list[WatchEvent]):
        self.catalog = {item.content_id: item for item in catalog}
        self.events = list(events)
        self.events_by_user: dict[str, list[WatchEvent]] = defaultdict(list)
        self.watchers_by_item: dict[str, set[str]] = defaultdict(set)
        for event in self.events:
            self.events_by_user[event.user_id].append(event)
            self.watchers_by_item[event.content_id].add(event.user_id)
        self.max_popularity = max((len(v) for v in self.watchers_by_item.values()), default=1)

    @staticmethod
    def _jaccard(a: set[str] | frozenset[str], b: set[str] | frozenset[str]) -> float:
        if not a and not b:
            return 0.0
        return len(a & b) / len(a | b)

    def _profile(self, user_events: list[WatchEvent]) -> Counter[str]:
        profile: Counter[str] = Counter()
        for event in user_events:
            item = self.catalog.get(event.content_id)
            if item is None:
                continue
            recency = 1.0 / (1.0 + event.days_ago / 30.0)
            weight = max(0.0, min(1.0, event.completion)) * recency
            for feature in item.features:
                profile[feature] += weight
        return profile

    @staticmethod
    def _cosine_profile(profile: Counter[str], features: frozenset[str]) -> float:
        if not profile or not features:
            return 0.0
        dot = sum(profile[f] for f in features)
        pnorm = math.sqrt(sum(v * v for v in profile.values()))
        fnorm = math.sqrt(len(features))
        return dot / (pnorm * fnorm) if pnorm and fnorm else 0.0

    def _collaborative(self, watched_ids: set[str], candidate_id: str) -> float:
        candidate_watchers = self.watchers_by_item[candidate_id]
        if not candidate_watchers:
            return 0.0
        best = 0.0
        for watched in watched_ids:
            best = max(best, self._jaccard(self.watchers_by_item[watched], candidate_watchers))
        return best

    def _popularity(self, content_id: str) -> float:
        viewers = len(self.watchers_by_item[content_id])
        return math.log1p(viewers) / math.log1p(self.max_popularity) if self.max_popularity else 0.0

    def _explanation(self, profile: Counter[str], item: ContentItem, components: tuple[float, float, float]) -> str:
        matches = sorted(item.features, key=lambda f: profile.get(f, 0.0), reverse=True)
        matches = [f.split(":", 1)[1] for f in matches if profile.get(f, 0.0) > 0][:2]
        reason = f"matches {', '.join(matches)}" if matches else "popular with similar viewers"
        c, collab, pop = components
        return f"{reason}; content={c:.2f}, collaborative={collab:.2f}, popularity={pop:.2f}"

    def _raw_candidates(self, user_id: str) -> list[Recommendation]:
        user_events = self.events_by_user.get(user_id, [])
        watched_ids = {e.content_id for e in user_events}
        profile = self._profile(user_events)
        out: list[Recommendation] = []
        for item in self.catalog.values():
            if item.content_id in watched_ids:
                continue
            content = self._cosine_profile(profile, item.features)
            collab = self._collaborative(watched_ids, item.content_id) if watched_ids else 0.0
            pop = self._popularity(item.content_id)
            if user_events:
                score = 0.50 * content + 0.35 * collab + 0.15 * pop
            else:
                score = pop
            out.append(
                Recommendation(
                    content_id=item.content_id,
                    title=item.title,
                    score=score,
                    content_score=content,
                    collaborative_score=collab,
                    popularity_score=pop,
                    explanation=self._explanation(profile, item, (content, collab, pop)),
                )
            )
        return sorted(out, key=lambda r: (-r.score, r.content_id))

    def recommend(self, user_id: str, k: int = 5, candidate_pool: int = 20, diversity_lambda: float = 0.78) -> list[Recommendation]:
        pool = self._raw_candidates(user_id)[:candidate_pool]
        selected: list[Recommendation] = []
        while pool and len(selected) < k:
            best = None
            best_mmr = float("-inf")
            for candidate in pool:
                if selected:
                    item = self.catalog[candidate.content_id]
                    max_similarity = max(
                        self._jaccard(item.features, self.catalog[s.content_id].features)
                        for s in selected
                    )
                else:
                    max_similarity = 0.0
                mmr = diversity_lambda * candidate.score - (1.0 - diversity_lambda) * max_similarity
                if mmr > best_mmr:
                    best = candidate
                    best_mmr = mmr
            selected.append(best)
            pool.remove(best)
        return selected
