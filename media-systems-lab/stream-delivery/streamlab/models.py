from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Rendition:
    bitrate_kbps: int
    width: int
    height: int
    name: str
    video_codec: str = "avc1.640028"
    audio_codec: str = "mp4a.40.2"


@dataclass(frozen=True)
class Segment:
    sequence: int
    duration: float
    uri: str
    size_bytes: int
