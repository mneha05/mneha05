from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass


@dataclass(frozen=True)
class CacheResult:
    hit: bool
    evictions: int


class EdgeCache:
    """Byte-capacity LRU cache with origin/edge accounting."""

    def __init__(self, capacity_bytes: int):
        if capacity_bytes <= 0:
            raise ValueError("capacity must be positive")
        self.capacity_bytes = capacity_bytes
        self._objects: OrderedDict[str, int] = OrderedDict()
        self._used = 0
        self.requests = 0
        self.hits = 0
        self.origin_bytes = 0
        self.edge_bytes = 0
        self.evictions = 0

    def request(self, key: str, size_bytes: int) -> CacheResult:
        self.requests += 1
        if key in self._objects:
            self.hits += 1
            self.edge_bytes += size_bytes
            self._objects.move_to_end(key)
            return CacheResult(True, 0)

        self.origin_bytes += size_bytes
        local_evictions = 0
        if size_bytes <= self.capacity_bytes:
            while self._objects and self._used + size_bytes > self.capacity_bytes:
                _, old_size = self._objects.popitem(last=False)
                self._used -= old_size
                self.evictions += 1
                local_evictions += 1
            self._objects[key] = size_bytes
            self._used += size_bytes
        return CacheResult(False, local_evictions)

    def metrics(self) -> dict[str, float | int]:
        total_bytes = self.edge_bytes + self.origin_bytes
        return {
            "requests": self.requests,
            "hit_rate": round(self.hits / self.requests, 4) if self.requests else 0.0,
            "byte_hit_rate": round(self.edge_bytes / total_bytes, 4) if total_bytes else 0.0,
            "origin_bytes": self.origin_bytes,
            "edge_bytes": self.edge_bytes,
            "evictions": self.evictions,
        }
