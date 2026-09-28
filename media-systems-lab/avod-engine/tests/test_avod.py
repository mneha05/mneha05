import unittest
from pathlib import Path

from avod.adapters import GoogleAdManagerStyleAdapter
from avod.decision import DecisionEngine
from avod.models import AdRequest, Campaign
from avod.ssai import splice_hls
from avod.tracking import EventLedger, TrackingEvent
from avod.vast import parse_vast


class AvodTests(unittest.TestCase):
    def setUp(self):
        self.request = AdRequest("r1", "u1", "US", "ctv", "action", "midroll", 10.0)

    def test_decision_respects_targeting_and_floor(self):
        good = Campaign("good", "A", "a.mp4", 15.0, 10.0, 0.9, frozenset({"US"}), frozenset({"ctv"}), frozenset({"action"}))
        wrong_geo = Campaign("geo", "B", "b.mp4", 50.0, 10.0, 1.0, frozenset({"CA"}))
        below_floor = Campaign("floor", "C", "c.mp4", 5.0, 10.0, 1.0)
        decision = DecisionEngine([good, wrong_geo, below_floor]).decide(self.request)
        self.assertEqual(decision.campaign_id, "good")

    def test_frequency_cap(self):
        c = Campaign("c", "A", "a.mp4", 20.0, 100.0, 1.0, frequency_cap=1)
        engine = DecisionEngine([c])
        self.assertIsNotNone(engine.decide(self.request))
        self.assertIsNone(engine.decide(self.request))

    def test_tracking_is_idempotent_and_computes_revenue(self):
        ledger = EventLedger()
        event = TrackingEvent("i1", "c1", "impression", 20.0)
        self.assertTrue(ledger.record(event))
        self.assertFalse(ledger.record(event))
        ledger.record(TrackingEvent("i1", "c1", "complete", 20.0))
        metrics = ledger.metrics("c1")
        self.assertEqual(metrics["impressions"], 1)
        self.assertEqual(metrics["completion_rate"], 1.0)
        self.assertEqual(metrics["revenue"], 0.02)

    def test_vast_parser(self):
        xml = (Path(__file__).parents[1] / "samples" / "vast.xml").read_text()
        creative = parse_vast(xml)
        self.assertEqual(creative.duration_seconds, 15)
        self.assertIn("complete", creative.trackers)
        self.assertTrue(creative.media_url.endswith("demo-720p.mp4"))

    def test_ssai_splice_adds_ad_and_discontinuities(self):
        playlist = """#EXTM3U\n#EXT-X-TARGETDURATION:6\n#EXTINF:6.0,\na.ts\n#EXTINF:6.0,\nb.ts\n#EXT-X-ENDLIST\n"""
        out = splice_hls(playlist, [("ad.ts", 5.0)], 1, "break-1")
        self.assertIn("ad.ts", out)
        self.assertEqual(out.count("#EXT-X-DISCONTINUITY"), 2)
        self.assertTrue(out.endswith("#EXT-X-ENDLIST\n"))

    def test_gam_adapter_contains_context(self):
        url = GoogleAdManagerStyleAdapter("/123/demo").build_request(self.request)["url"]
        self.assertIn("output=vast", url)
        self.assertIn("correlator=r1", url)


if __name__ == "__main__":
    unittest.main()
