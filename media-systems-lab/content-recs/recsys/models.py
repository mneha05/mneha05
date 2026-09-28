from dataclasses import dataclass


@dataclass(frozen=True)
class ContentItem:
    content_id: str
    title: str
    genres: frozenset[str]
    tags: frozenset[str]
    year: int

    @property
    def features(self) -> frozenset[str]:
        return frozenset({*(f"genre:{g}" for g in self.genres), *(f"tag:{t}" for t in self.tags)})


@dataclass(frozen=True)
class WatchEvent:
    user_id: str
    content_id: str
    completion: float
    days_ago: int
