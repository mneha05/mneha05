from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class AdRequest:
    request_id: str
    user_id: str
    country: str
    device: str
    genre: str
    placement: str
    floor_cpm: float = 0.0


@dataclass
class Campaign:
    campaign_id: str
    advertiser: str
    creative_url: str
    cpm: float
    budget: float
    predicted_completion_rate: float
    countries: FrozenSet[str] = field(default_factory=frozenset)
    devices: FrozenSet[str] = field(default_factory=frozenset)
    genres: FrozenSet[str] = field(default_factory=frozenset)
    frequency_cap: int = 3
    spent: float = 0.0
    impressions: int = 0
    target_impressions: int = 1000

    @property
    def remaining_budget(self) -> float:
        return max(0.0, self.budget - self.spent)

    @property
    def cost_per_impression(self) -> float:
        return self.cpm / 1000.0


@dataclass(frozen=True)
class Decision:
    request_id: str
    campaign_id: str
    advertiser: str
    creative_url: str
    bid_cpm: float
    quality_adjusted_cpm: float
    reason: str
