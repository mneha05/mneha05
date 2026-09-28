from __future__ import annotations

from dataclasses import dataclass
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class VastCreative:
    ad_id: str
    duration_seconds: int
    media_url: str
    impression_url: str | None
    click_through_url: str | None
    trackers: dict[str, tuple[str, ...]]


def _seconds(duration: str) -> int:
    h, m, s = duration.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(float(s))


def parse_vast(xml_text: str) -> VastCreative:
    root = ET.fromstring(xml_text)
    ad = root.find("./Ad")
    if ad is None:
        raise ValueError("VAST document has no Ad")

    linear = ad.find(".//Linear")
    if linear is None:
        raise ValueError("VAST document has no Linear creative")

    duration_node = linear.find("./Duration")
    media = linear.find(".//MediaFile")
    if duration_node is None or not duration_node.text or media is None or not media.text:
        raise ValueError("VAST linear creative is missing duration or media")

    trackers: dict[str, list[str]] = {}
    for node in linear.findall(".//Tracking"):
        event = node.attrib.get("event", "unknown")
        if node.text and node.text.strip():
            trackers.setdefault(event, []).append(node.text.strip())

    impression = ad.find(".//Impression")
    click = linear.find(".//ClickThrough")
    return VastCreative(
        ad_id=ad.attrib.get("id", "unknown"),
        duration_seconds=_seconds(duration_node.text),
        media_url=media.text.strip(),
        impression_url=impression.text.strip() if impression is not None and impression.text else None,
        click_through_url=click.text.strip() if click is not None and click.text else None,
        trackers={k: tuple(v) for k, v in trackers.items()},
    )


def csai_payload(creative: VastCreative) -> dict[str, object]:
    return {
        "ad_id": creative.ad_id,
        "media_url": creative.media_url,
        "duration_seconds": creative.duration_seconds,
        "impression": creative.impression_url,
        "tracking": creative.trackers,
        "click_through": creative.click_through_url,
    }
