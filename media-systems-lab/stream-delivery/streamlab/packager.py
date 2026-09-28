from __future__ import annotations

from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

from .models import Rendition


def hls_master(renditions: list[Rendition]) -> str:
    lines = ["#EXTM3U", "#EXT-X-VERSION:7"]
    for r in sorted(renditions):
        bandwidth = r.bitrate_kbps * 1000
        lines.append(
            f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={r.width}x{r.height},CODECS="{r.video_codec},{r.audio_codec}"'
        )
        lines.append(f"{r.name}/index.m3u8")
    return "\n".join(lines) + "\n"


def hls_media(rendition: Rendition, segment_count: int = 6, segment_duration: float = 6.0) -> str:
    target = int(segment_duration) if segment_duration.is_integer() else int(segment_duration) + 1
    lines = [
        "#EXTM3U",
        "#EXT-X-VERSION:7",
        f"#EXT-X-TARGETDURATION:{target}",
        "#EXT-X-MEDIA-SEQUENCE:0",
    ]
    for i in range(segment_count):
        lines.extend((f"#EXTINF:{segment_duration:.3f},", f"segment-{i:05d}.m4s"))
    lines.append("#EXT-X-ENDLIST")
    return "\n".join(lines) + "\n"


def dash_mpd(renditions: list[Rendition], duration_seconds: int = 36, segment_seconds: int = 6) -> str:
    mpd = Element(
        "MPD",
        {
            "xmlns": "urn:mpeg:dash:schema:mpd:2011",
            "type": "static",
            "mediaPresentationDuration": f"PT{duration_seconds}S",
            "minBufferTime": "PT1.5S",
        },
    )
    period = SubElement(mpd, "Period", {"id": "p0", "start": "PT0S"})
    adaptation = SubElement(period, "AdaptationSet", {"mimeType": "video/mp4", "segmentAlignment": "true"})
    for r in sorted(renditions):
        rep = SubElement(
            adaptation,
            "Representation",
            {
                "id": r.name,
                "bandwidth": str(r.bitrate_kbps * 1000),
                "width": str(r.width),
                "height": str(r.height),
                "codecs": r.video_codec,
            },
        )
        SubElement(
            rep,
            "SegmentTemplate",
            {
                "timescale": "1",
                "duration": str(segment_seconds),
                "startNumber": "0",
                "initialization": "init.mp4",
                "media": "segment-$Number%05d$.m4s",
            },
        )
    return tostring(mpd, encoding="unicode")


def ffmpeg_commands(input_path: str, output_dir: str, renditions: list[Rendition]) -> list[list[str]]:
    commands: list[list[str]] = []
    for r in sorted(renditions):
        out = str(Path(output_dir) / r.name / "index.m3u8")
        commands.append(
            [
                "ffmpeg",
                "-y",
                "-i",
                input_path,
                "-vf",
                f"scale=w={r.width}:h={r.height}:force_original_aspect_ratio=decrease",
                "-c:v",
                "libx264",
                "-b:v",
                f"{r.bitrate_kbps}k",
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-hls_time",
                "6",
                "-hls_playlist_type",
                "vod",
                "-hls_segment_type",
                "fmp4",
                out,
            ]
        )
    return commands
