from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

VALID_EVENTS = {
    "impression",
    "start",
    "firstQuartile",
    "midpoint",
    "thirdQuartile",
    "complete",
    "click",
}


@dataclass(frozen=True)
class TrackingEvent:
    impression_id: str
    campaign_id: str
    event_type: str
    cpm: float


class EventLedger:
    """Idempotent in-memory event collector with CPM-derived revenue metrics."""

    def __init__(self):
        self._seen: set[tuple[str, str]] = set()
        self._counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._revenue: dict[str, float] = defaultdict(float)

    def record(self, event: TrackingEvent) -> bool:
        if event.event_type not in VALID_EVENTS:
            raise ValueError(f"unsupported event: {event.event_type}")
        key = (event.impression_id, event.event_type)
        if key in self._seen:
            return False
        self._seen.add(key)
        self._counts[event.campaign_id][event.event_type] += 1
        if event.event_type == "impression":
            self._revenue[event.campaign_id] += event.cpm / 1000.0
        return True

    def metrics(self, campaign_id: str) -> dict[str, float | int]:
        c = self._counts[campaign_id]
        impressions = c["impression"]
        completes = c["complete"]
        clicks = c["click"]
        return {
            "impressions": impressions,
            "completions": completes,
            "clicks": clicks,
            "completion_rate": round(completes / impressions, 4) if impressions else 0.0,
            "ctr": round(clicks / impressions, 4) if impressions else 0.0,
            "revenue": round(self._revenue[campaign_id], 6),
        }
