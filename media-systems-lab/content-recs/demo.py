from recsys.engine import HybridRecommender
from recsys.evaluate import evaluate_leave_one_out
from recsys.models import ContentItem, WatchEvent


def data():
    catalog = [
        ContentItem("c1", "Orbital Rescue", frozenset({"sci-fi", "action"}), frozenset({"space", "survival"}), 2025),
        ContentItem("c2", "Redline Unit", frozenset({"action", "thriller"}), frozenset({"cars", "heist"}), 2024),
        ContentItem("c3", "Moonbase Nine", frozenset({"sci-fi", "drama"}), frozenset({"space", "mystery"}), 2026),
        ContentItem("c4", "Laugh Track", frozenset({"comedy"}), frozenset({"workplace", "ensemble"}), 2023),
        ContentItem("c5", "Deep Current", frozenset({"documentary"}), frozenset({"ocean", "nature"}), 2025),
        ContentItem("c6", "Night Signal", frozenset({"thriller", "sci-fi"}), frozenset({"mystery", "technology"}), 2026),
        ContentItem("c7", "Pit Lane", frozenset({"sports", "documentary"}), frozenset({"cars", "racing"}), 2024),
        ContentItem("c8", "After Hours", frozenset({"comedy", "drama"}), frozenset({"workplace", "friendship"}), 2025),
    ]
    events = [
        WatchEvent("u1", "c1", 1.0, 20), WatchEvent("u1", "c2", 0.9, 10), WatchEvent("u1", "c3", 1.0, 1),
        WatchEvent("u2", "c1", 0.9, 30), WatchEvent("u2", "c3", 0.95, 12), WatchEvent("u2", "c6", 1.0, 2),
        WatchEvent("u3", "c2", 1.0, 22), WatchEvent("u3", "c7", 0.9, 3),
        WatchEvent("u4", "c4", 1.0, 25), WatchEvent("u4", "c8", 0.95, 2),
        WatchEvent("u5", "c5", 0.9, 15), WatchEvent("u5", "c7", 1.0, 1),
        WatchEvent("u6", "c1", 1.0, 40), WatchEvent("u6", "c3", 0.8, 8), WatchEvent("u6", "c6", 0.9, 1),
    ]
    return catalog, events


def main() -> None:
    catalog, events = data()
    engine = HybridRecommender(catalog, events)

    print("=== PERSONALIZED RECOMMENDATIONS: u1 ===")
    for rank, rec in enumerate(engine.recommend("u1", k=4), start=1):
        print(f"{rank}. {rec.title:<16} score={rec.score:.3f} | {rec.explanation}")

    print("\n=== COLD START ===")
    for rank, rec in enumerate(engine.recommend("new-viewer", k=3), start=1):
        print(f"{rank}. {rec.title:<16} score={rec.score:.3f}")

    print("\n=== OFFLINE EVALUATION ===")
    print(evaluate_leave_one_out(catalog, events, k=3))


if __name__ == "__main__":
    main()
