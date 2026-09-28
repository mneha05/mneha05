from __future__ import annotations


def splice_hls(content_playlist: str, ad_segments: list[tuple[str, float]], after_segment: int, break_id: str) -> str:
    """Insert ad media into a simple HLS media playlist after N content segments."""
    lines = [line.strip() for line in content_playlist.strip().splitlines() if line.strip()]
    header: list[str] = []
    segments: list[tuple[str, str]] = []
    pending_extinf: str | None = None
    footer: list[str] = []

    for line in lines:
        if line.startswith("#EXTINF:"):
            pending_extinf = line
        elif pending_extinf and not line.startswith("#"):
            segments.append((pending_extinf, line))
            pending_extinf = None
        elif line == "#EXT-X-ENDLIST":
            footer.append(line)
        elif not segments and pending_extinf is None:
            header.append(line)
        elif line.startswith("#"):
            footer.append(line)

    if after_segment < 0 or after_segment > len(segments):
        raise ValueError("after_segment outside content segment range")

    out = list(header)
    for idx, (extinf, uri) in enumerate(segments, start=1):
        out.extend((extinf, uri))
        if idx == after_segment:
            out.append(f'#EXT-X-DATERANGE:ID="{break_id}",CLASS="avod-ad-break"')
            out.append("#EXT-X-DISCONTINUITY")
            for ad_uri, duration in ad_segments:
                out.extend((f"#EXTINF:{duration:.3f},", ad_uri))
            out.append("#EXT-X-DISCONTINUITY")

    if "#EXT-X-ENDLIST" in footer:
        out.append("#EXT-X-ENDLIST")
    return "\n".join(out) + "\n"
