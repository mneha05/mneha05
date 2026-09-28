from __future__ import annotations

from collections import deque
from statistics import harmonic_mean

from .models import Rendition


class ThroughputAbr:
    def __init__(self, renditions: list[Rendition], history: int = 5, safety: float = 0.80):
        if not renditions:
            raise ValueError("at least one rendition required")
        self.renditions = sorted(renditions)
        self.samples_kbps: deque[float] = deque(maxlen=history)
        self.safety = safety

    def add_sample(self, bytes_downloaded: int, seconds: float) -> float:
        if seconds <= 0:
            raise ValueError("seconds must be > 0")
        kbps = (bytes_downloaded * 8.0 / 1000.0) / seconds
        self.samples_kbps.append(kbps)
        return kbps

    def estimated_kbps(self) -> float | None:
        return harmonic_mean(self.samples_kbps) if self.samples_kbps else None

    def choose(self) -> Rendition:
        estimate = self.estimated_kbps()
        if estimate is None:
            return self.renditions[0]
        safe = estimate * self.safety
        candidates = [r for r in self.renditions if r.bitrate_kbps <= safe]
        return candidates[-1] if candidates else self.renditions[0]
