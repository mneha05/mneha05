from __future__ import annotations

from collections import defaultdict
from datetime import date
from math import sqrt

def dedupe(events: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for event in events:
        by_id[event["event_id"]] = event
    return list(by_id.values())

def daily_active_users(events: list[dict]) -> dict[str, int]:
    users: dict[str, set[str]] = defaultdict(set)
    for e in dedupe(events):
        users[e["event_date"]].add(e["user_id"])
    return {day: len(ids) for day, ids in sorted(users.items())}

def funnel(events: list[dict]) -> dict[str, float | int]:
    seen: dict[str, set[str]] = defaultdict(set)
    for e in dedupe(events):
        seen[e["event_name"]].add(e["user_id"])
    opened, feature = len(seen["app_open"]), len(seen["feature_view"])
    liked, shared = len(seen["like"]), len(seen["share"])
    return {
        "app_open_users": opened,
        "feature_view_users": feature,
        "like_users": liked,
        "share_users": shared,
        "feature_adoption": round(feature / opened, 4) if opened else 0.0,
        "feature_to_like": round(liked / feature, 4) if feature else 0.0,
    }

def retention(events: list[dict], day_n: int = 1) -> float:
    user_days: dict[str, list[date]] = defaultdict(list)
    for e in dedupe(events):
        d = date.fromisoformat(e["event_date"])
        if d not in user_days[e["user_id"]]:
            user_days[e["user_id"]].append(d)
    eligible = retained = 0
    for days in user_days.values():
        days = sorted(days)
        if not days:
            continue
        target = days[0].toordinal() + day_n
        eligible += 1
        if any(d.toordinal() == target for d in days):
            retained += 1
    return round(retained / eligible, 4) if eligible else 0.0

def experiment_metrics(events: list[dict]) -> dict[str, dict[str, float | int]]:
    opened: dict[str, set[str]] = defaultdict(set)
    converted: dict[str, set[str]] = defaultdict(set)
    for e in dedupe(events):
        arm = e["experiment_arm"]
        if e["event_name"] == "app_open":
            opened[arm].add(e["user_id"])
        if e["event_name"] == "feature_view":
            converted[arm].add(e["user_id"])
    out = {}
    for arm in sorted(set(opened) | set(converted)):
        n, c = len(opened[arm]), len(converted[arm])
        out[arm] = {"users": n, "converters": c, "conversion": round(c / n, 4) if n else 0.0}
    if "control" in out and "treatment" in out:
        pc, pt = float(out["control"]["conversion"]), float(out["treatment"]["conversion"])
        nc, nt = int(out["control"]["users"]), int(out["treatment"]["users"])
        pooled = ((pc * nc) + (pt * nt)) / max(1, nc + nt)
        se = sqrt(max(1e-12, pooled * (1 - pooled) * ((1 / max(1, nc)) + (1 / max(1, nt)))))
        out["summary"] = {
            "absolute_lift": round(pt - pc, 4),
            "relative_lift": round((pt / pc) - 1, 4) if pc else 0.0,
            "z_score": round((pt - pc) / se, 3),
        }
    return out
