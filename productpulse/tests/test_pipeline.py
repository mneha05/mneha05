import json
import tempfile
import unittest
from pathlib import Path

from analytics.oracle import daily_active_users, dedupe, experiment_metrics, funnel, retention
from generator.generate_events import generate_events, write_jsonl

class ProductPulseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = generate_events(users=400, days=10, seed=11)

    def test_generator_is_deterministic(self):
        self.assertEqual(self.events, generate_events(users=400, days=10, seed=11))

    def test_event_ids_are_deduplicated(self):
        unique = dedupe(self.events)
        self.assertLess(len(unique), len(self.events))
        self.assertEqual(len({e["event_id"] for e in unique}), len(unique))

    def test_jsonl_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "events.jsonl"
            write_jsonl(p, self.events[:25])
            rows = [json.loads(line) for line in p.read_text().splitlines()]
            self.assertEqual(rows, self.events[:25])

    def test_dau_is_positive(self):
        dau = daily_active_users(self.events)
        self.assertGreater(len(dau), 3)
        self.assertTrue(all(v > 0 for v in dau.values()))

    def test_funnel_is_monotonic(self):
        f = funnel(self.events)
        self.assertGreaterEqual(f["app_open_users"], f["feature_view_users"])
        self.assertGreaterEqual(f["feature_view_users"], f["like_users"])
        self.assertGreaterEqual(f["like_users"], f["share_users"])

    def test_retention_is_bounded(self):
        r = retention(self.events, 1)
        self.assertGreaterEqual(r, 0.0)
        self.assertLessEqual(r, 1.0)

    def test_treatment_has_higher_feature_conversion(self):
        m = experiment_metrics(self.events)
        self.assertGreater(m["treatment"]["conversion"], m["control"]["conversion"])
        self.assertGreater(m["summary"]["absolute_lift"], 0)

if __name__ == "__main__":
    unittest.main()
