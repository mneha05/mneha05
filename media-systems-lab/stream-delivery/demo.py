from streamlab.abr import ThroughputAbr
from streamlab.cdn import EdgeCache
from streamlab.live import LiveWindow
from streamlab.models import Rendition, Segment
from streamlab.packager import dash_mpd, ffmpeg_commands, hls_master


LADDER = [
    Rendition(600, 640, 360, "360p"),
    Rendition(1400, 854, 480, "480p"),
    Rendition(2800, 1280, 720, "720p"),
    Rendition(5000, 1920, 1080, "1080p"),
]


def main() -> None:
    print("=== HLS MASTER ===")
    print(hls_master(LADDER))

    print("=== DASH MPD ===")
    print(dash_mpd(LADDER))

    print("\n=== FFMPEG PLAN (720p) ===")
    print(" ".join(ffmpeg_commands("input.mp4", "out", LADDER)[2]))

    print("\n=== ABR ===")
    abr = ThroughputAbr(LADDER)
    for bytes_downloaded, seconds in [(2_000_000, 4.0), (1_800_000, 4.0), (1_250_000, 4.0)]:
        sample = abr.add_sample(bytes_downloaded, seconds)
        print(f"sample={sample:.0f} kbps -> selected={abr.choose().name}")

    live = LiveWindow(window_size=3)
    for seq in range(100, 105):
        live.append(Segment(seq, 6.0, f"live-{seq}.m4s", 900_000))
    print("\n=== LIVE WINDOW ===")
    print(live.playlist())

    cache = EdgeCache(capacity_bytes=3_000_000)
    trace = [
        ("720/seg-1", 900_000),
        ("720/seg-2", 900_000),
        ("720/seg-1", 900_000),
        ("480/seg-1", 500_000),
        ("720/seg-3", 900_000),
        ("720/seg-1", 900_000),
        ("480/seg-1", 500_000),
    ]
    for key, size in trace:
        cache.request(key, size)
    print("=== CDN METRICS ===")
    print(cache.metrics())


if __name__ == "__main__":
    main()
