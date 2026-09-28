from __future__ import annotations

from collections import deque

from .models import Segment


class LiveWindow:
    def __init__(self, target_duration: int = 6, window_size: int = 5):
        self.target_duration = target_duration
        self.window_size = window_size
        self._segments: deque[Segment] = deque(maxlen=window_size)

    def append(self, segment: Segment) -> None:
        if self._segments and segment.sequence <= self._segments[-1].sequence:
            raise ValueError("live segment sequence must increase")
        self._segments.append(segment)

    def playlist(self) -> str:
        sequence = self._segments[0].sequence if self._segments else 0
        lines = [
            "#EXTM3U",
            "#EXT-X-VERSION:7",
            f"#EXT-X-TARGETDURATION:{self.target_duration}",
            f"#EXT-X-MEDIA-SEQUENCE:{sequence}",
        ]
        for s in self._segments:
            lines.extend((f"#EXTINF:{s.duration:.3f},", s.uri))
        return "\n".join(lines) + "\n"
