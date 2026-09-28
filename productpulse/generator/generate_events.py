from __future__ import annotations

import argparse
import json
import random
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

COUNTRIES = ("US", "IN", "BR", "GB", "CA")
PLATFORMS = ("ios", "android", "web")

@dataclass(frozen=True)
class Event:
    event_id: str
    user_id: str
    event_name: str
    event_ts: str
    event_date: str
    session_id: str
    country: str
    platform: str
    experiment_arm: str
    feature_name: str | None

def _event_id(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, seed))

def generate_events(users: int = 2000, days: int = 14, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    start = datetime(2026, 9, 1, tzinfo=timezone.utc)
    out: list[dict] = []
    for u in range(users):
        user_id = f"u{u:06d}"
        arm = "treatment" if u % 2 else "control"
        country = COUNTRIES[u % len(COUNTRIES)]
        platform = PLATFORMS[(u // len(COUNTRIES)) % len(PLATFORMS)]
        signup_day = rng.randrange(max(1, days // 3))
        activity_bias = 0.55 + (u % 11) / 30.0
        for day in range(signup_day, days):
            if rng.random() > min(0.94, activity_bias):
                continue
            sessions = 1 + int(rng.random() < 0.18)
            for s in range(sessions):
                session_id = f"{user_id}-d{day:02d}-s{s}"
                base = start + timedelta(days=day, hours=8 + rng.randrange(12), minutes=rng.randrange(60))
                names = ["app_open", "feed_view"]
                feature_prob = 0.42 if arm == "treatment" else 0.30
                if rng.random() < feature_prob:
                    names.append("feature_view")
                    if rng.random() < (0.28 if arm == "treatment" else 0.20):
                        names.append("like")
                    if rng.random() < (0.09 if arm == "treatment" else 0.06):
                        names.append("share")
                for i, name in enumerate(names):
                    ts = base + timedelta(seconds=15 * i + rng.randrange(8))
                    out.append(asdict(Event(
                        event_id=_event_id(f"{seed}:{session_id}:{name}:{i}"),
                        user_id=user_id,
                        event_name=name,
                        event_ts=ts.isoformat(),
                        event_date=ts.date().isoformat(),
                        session_id=session_id,
                        country=country,
                        platform=platform,
                        experiment_arm=arm,
                        feature_name="short_video" if name in {"feature_view", "like", "share"} else None,
                    )))
    if out:
        out.extend(dict(out[i]) for i in range(0, min(len(out), 200), 40))
        late = dict(out[min(10, len(out)-1)])
        late["event_id"] = _event_id(f"{seed}:late-arrival")
        late["event_ts"] = (datetime.fromisoformat(late["event_ts"]) - timedelta(days=2)).isoformat()
        late["event_date"] = datetime.fromisoformat(late["event_ts"]).date().isoformat()
        out.append(late)
    return out

def write_jsonl(path: Path, events: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, separators=(",", ":")) + "\n")

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--users", type=int, default=2000)
    p.add_argument("--days", type=int, default=14)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--out", type=Path, default=Path("data/events.jsonl"))
    args = p.parse_args()
    events = generate_events(args.users, args.days, args.seed)
    write_jsonl(args.out, events)
    print(f"wrote {len(events):,} events to {args.out}")

if __name__ == "__main__":
    main()
