from pathlib import Path

from avod.adapters import FreeWheelStyleAdapter, GoogleAdManagerStyleAdapter
from avod.decision import DecisionEngine
from avod.models import AdRequest, Campaign
from avod.ssai import splice_hls
from avod.tracking import EventLedger, TrackingEvent
from avod.vast import csai_payload, parse_vast


def main() -> None:
    campaigns = [
        Campaign(
            campaign_id="auto-18",
            advertiser="RoadRunner Motors",
            creative_url="https://cdn.example/ads/auto-18.mp4",
            cpm=18.0,
            budget=500.0,
            predicted_completion_rate=0.91,
            countries=frozenset({"US"}),
            devices=frozenset({"ctv", "web"}),
            genres=frozenset({"action", "sports"}),
            frequency_cap=2,
            target_impressions=20000,
        ),
        Campaign(
            campaign_id="snack-21",
            advertiser="CrunchCo",
            creative_url="https://cdn.example/ads/snack-21.mp4",
            cpm=21.0,
            budget=450.0,
            predicted_completion_rate=0.62,
            countries=frozenset({"US"}),
            devices=frozenset({"ctv"}),
            genres=frozenset({"action", "comedy"}),
            frequency_cap=3,
            target_impressions=18000,
        ),
    ]
    request = AdRequest(
        request_id="req-1042",
        user_id="viewer-17",
        country="US",
        device="ctv",
        genre="action",
        placement="midroll-1",
        floor_cpm=12.0,
    )

    engine = DecisionEngine(campaigns)
    decision = engine.decide(request)
    assert decision is not None
    engine.settle_impression(decision.campaign_id)

    print("=== AD DECISION ===")
    print(decision)

    print("\n=== AD SERVER ADAPTERS ===")
    print("FreeWheel-style:", FreeWheelStyleAdapter("12345", "ott_us").build_request(request))
    print("GAM-style:", GoogleAdManagerStyleAdapter("/1234/avod/midroll").build_request(request))

    vast_xml = (Path(__file__).parent / "samples" / "vast.xml").read_text()
    creative = parse_vast(vast_xml)
    print("\n=== CSAI VAST PAYLOAD ===")
    print(csai_payload(creative))

    content = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:6
#EXTINF:6.000,
content-000.ts
#EXTINF:6.000,
content-001.ts
#EXTINF:6.000,
content-002.ts
#EXTINF:6.000,
content-003.ts
#EXT-X-ENDLIST
"""
    stitched = splice_hls(
        content,
        [("ad-000.ts", 5.0), ("ad-001.ts", 5.0), ("ad-002.ts", 5.0)],
        after_segment=2,
        break_id="midroll-1",
    )
    print("\n=== SSAI PLAYLIST ===")
    print(stitched)

    ledger = EventLedger()
    for event_type in ("impression", "start", "firstQuartile", "midpoint", "thirdQuartile", "complete", "click"):
        ledger.record(TrackingEvent("imp-9001", decision.campaign_id, event_type, decision.bid_cpm))
    # Duplicate beacon retry is ignored.
    ledger.record(TrackingEvent("imp-9001", decision.campaign_id, "impression", decision.bid_cpm))
    print("=== TRACKING METRICS ===")
    print(ledger.metrics(decision.campaign_id))


if __name__ == "__main__":
    main()
