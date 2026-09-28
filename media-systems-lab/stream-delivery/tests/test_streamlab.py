import unittest
from xml.etree import ElementTree as ET

from streamlab.abr import ThroughputAbr
from streamlab.cdn import EdgeCache
from streamlab.live import LiveWindow
from streamlab.models import Rendition, Segment
from streamlab.packager import dash_mpd, ffmpeg_commands, hls_master, hls_media


class StreamLabTests(unittest.TestCase):
    def setUp(self):
        self.ladder = [
            Rendition(600, 640, 360, "360p"),
            Rendition(2800, 1280, 720, "720p"),
            Rendition(5000, 1920, 1080, "1080p"),
        ]

    def test_hls_master_contains_every_rendition(self):
        text = hls_master(self.ladder)
        self.assertIn("360p/index.m3u8", text)
        self.assertIn("1080p/index.m3u8", text)
        self.assertEqual(text.count("#EXT-X-STREAM-INF"), 3)

    def test_hls_media_is_vod(self):
        text = hls_media(self.ladder[0], segment_count=3)
        self.assertEqual(text.count("#EXTINF"), 3)
        self.assertIn("#EXT-X-ENDLIST", text)

    def test_dash_is_well_formed_xml(self):
        xml = dash_mpd(self.ladder)
        root = ET.fromstring(xml)
        self.assertTrue(root.tag.endswith("MPD"))
        self.assertEqual(xml.count("Representation"), 6)  # open + close tags

    def test_abr_selects_highest_safe_rendition(self):
        abr = ThroughputAbr(self.ladder, safety=0.8)
        abr.add_sample(2_000_000, 4.0)  # 4000 kbps => 3200 safe
        self.assertEqual(abr.choose().name, "720p")

    def test_live_window_rolls_sequence(self):
        live = LiveWindow(window_size=2)
        for seq in range(10, 13):
            live.append(Segment(seq, 6.0, f"{seq}.m4s", 100))
        text = live.playlist()
        self.assertIn("#EXT-X-MEDIA-SEQUENCE:11", text)
        self.assertNotIn("10.m4s", text)
        self.assertNotIn("ENDLIST", text)

    def test_cdn_cache_hits_and_evicts(self):
        cache = EdgeCache(200)
        cache.request("a", 100)
        cache.request("b", 100)
        self.assertTrue(cache.request("a", 100).hit)
        cache.request("c", 150)
        metrics = cache.metrics()
        self.assertGreater(metrics["hit_rate"], 0)
        self.assertGreaterEqual(metrics["evictions"], 1)

    def test_ffmpeg_plan_contains_transcode_settings(self):
        cmd = ffmpeg_commands("input.mp4", "out", [self.ladder[1]])[0]
        joined = " ".join(cmd)
        self.assertIn("libx264", joined)
        self.assertIn("2800k", joined)
        self.assertIn("-hls_segment_type fmp4", joined)


if __name__ == "__main__":
    unittest.main()
