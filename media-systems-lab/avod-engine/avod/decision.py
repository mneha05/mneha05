from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import AdRequest, Campaign, Decision


class DecisionEngine:
    """In-memory ad decision engine with deterministic targeting and pacing."""

    def __init__(self, campaigns: Iterable[Campaign]):
        self.campaigns = {c.campaign_id: c for c in campaigns}
        self._user_frequency: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    @staticmethod
    def _matches(value: str, allowed: frozenset[str]) -> bool:
        return not allowed or value in allowed

    def _eligible(self, request: AdRequest, campaign: Campaign) -> bool:
        return all(
            (
                campaign.cpm >= request.floor_cpm,
                campaign.remaining_budget >= campaign.cost_per_impression,
                self._matches(request.country, campaign.countries),
                self._matches(request.device, campaign.devices),
                self._matches(request.genre, campaign.genres),
                self._user_frequency[request.user_id][campaign.campaign_id]
                < campaign.frequency_cap,
            )
        )

    @staticmethod
    def _pacing_multiplier(campaign: Campaign) -> float:
        """Boost under-delivery and damp over-delivery without changing eligibility."""
        budget_progress = campaign.spent / campaign.budget if campaign.budget else 1.0
        delivery_progress = (
            campaign.impressions / campaign.target_impressions
            if campaign.target_impressions
            else 1.0
        )
        ratio = (budget_progress + 0.10) / (delivery_progress + 0.10)
        return max(0.80, min(1.20, ratio))

    def _score(self, campaign: Campaign) -> float:
        quality = 0.65 + 0.35 * max(0.0, min(1.0, campaign.predicted_completion_rate))
        return campaign.cpm * quality * self._pacing_multiplier(campaign)

    def decide(self, request: AdRequest) -> Decision | None:
        eligible = [c for c in self.campaigns.values() if self._eligible(request, c)]
        if not eligible:
            return None

        winner = max(eligible, key=lambda c: (self._score(c), c.cpm, c.campaign_id))
        score = self._score(winner)
        self._user_frequency[request.user_id][winner.campaign_id] += 1
        return Decision(
            request_id=request.request_id,
            campaign_id=winner.campaign_id,
            advertiser=winner.advertiser,
            creative_url=winner.creative_url,
            bid_cpm=winner.cpm,
            quality_adjusted_cpm=round(score, 4),
            reason="highest eligible quality-adjusted CPM after targeting, budget, floor, and frequency-cap checks",
        )

    def settle_impression(self, campaign_id: str) -> None:
        campaign = self.campaigns[campaign_id]
        if campaign.remaining_budget < campaign.cost_per_impression:
            raise ValueError("campaign budget exhausted")
        campaign.impressions += 1
        campaign.spent = round(campaign.spent + campaign.cost_per_impression, 8)

    def frequency(self, user_id: str, campaign_id: str) -> int:
        return self._user_frequency[user_id][campaign_id]
