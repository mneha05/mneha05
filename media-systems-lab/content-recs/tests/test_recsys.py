import unittest

from recsys.engine import HybridRecommender
from recsys.evaluate import evaluate_leave_one_out
from recsys.models import ContentItem, WatchEvent


class RecsysTests(unittest.TestCase):
    def setUp(self):
        self.catalog = [
            ContentItem("a", "A", frozenset({"sci-fi"}), frozenset({"space"}), 2025),
            ContentItem("b", "B", frozenset({"sci-fi"}), frozenset({"space", "mystery"}), 2025),
            ContentItem("c", "C", frozenset({"comedy"}), frozenset({"workplace"}), 2025),
            ContentItem("d", "D", frozenset({"thriller"}), frozenset({"mystery"}), 2025),
        ]
        self.events = [
            WatchEvent("u1", "a", 1.0, 10), WatchEvent("u1", "b", 1.0, 1),
            WatchEvent("u2", "a", 1.0, 9), WatchEvent("u2", "b", 1.0, 2),
            WatchEvent("u3", "c", 1.0, 7), WatchEvent("u3", "d", 1.0, 1),
        ]

    def test_seen_items_are_filtered(self):
        engine = HybridRecommender(self.catalog, self.events)
        ids = [r.content_id for r in engine.recommend("u1", k=4)]
        self.assertNotIn("a", ids)
        self.assertNotIn("b", ids)

    def test_content_affinity_prefers_related_item(self):
        training = [WatchEvent("u1", "a", 1.0, 1)]
        engine = HybridRecommender(self.catalog, training)
        self.assertEqual(engine.recommend("u1", k=1)[0].content_id, "b")

    def test_cold_start_returns_popular_items(self):
        engine = HybridRecommender(self.catalog, self.events)
        recs = engine.recommend("new", k=2)
        self.assertEqual(len(recs), 2)
        self.assertTrue(all(r.popularity_score > 0 for r in recs))

    def test_evaluation_metrics_are_bounded(self):
        metrics = evaluate_leave_one_out(self.catalog, self.events, k=2)
        self.assertGreaterEqual(metrics["recall@2"], 0.0)
        self.assertLessEqual(metrics["recall@2"], 1.0)
        self.assertGreaterEqual(metrics["ndcg@2"], 0.0)
        self.assertLessEqual(metrics["ndcg@2"], 1.0)
        self.assertGreater(metrics["catalog_coverage"], 0.0)


if __name__ == "__main__":
    unittest.main()
