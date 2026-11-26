"""Fetch subtitles via yt-dlp and clean them into readable plain text."""

from __future__ import annotations

import argparse
import glob
import os
import re
import subprocess
import sys
from pathlib import Path


def clean_subtitle_text(raw: str) -> str:
    lines: list[str] = []
    seen_recent: list[str] = []
    for line in raw.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")):
            continue
        if re.fullmatch(r"\d+", s):
            continue
        if "-->" in s:
            continue
        # Strip inline VTT/ASS tags
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"\{\\[^}]+\}", "", s)
        s = s.strip()
        if not s:
            continue
        if s in seen_recent:
            continue
        lines.append(s)
        seen_recent.append(s)
        if len(seen_recent) > 3:
            seen_recent.pop(0)
    return "\n".join(lines) + ("\n" if lines else "")


def main() -> int:
    parser = argparse.ArgumentParser(description="Download and clean video subtitles via yt-dlp.")
    parser.add_argument("url", help="Video URL (Bilibili, YouTube, etc.)")
    parser.add_argument("--out", default=".", help="Output directory")
    parser.add_argument("--langs", default="zh-Hans,zh-CN,zh,en", help="Preferred subtitle languages")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    template = str(out_dir / "%(title).80s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        args.langs,
        "--sub-format",
        "srt/vtt/best",
        "-o",
        template,
        args.url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        return proc.returncode

    sub_files = []
    for ext in ("*.srt", "*.vtt", "*.ass"):
        sub_files.extend(glob.glob(str(out_dir / ext)))

    if not sub_files:
        print("NO_SUBTITLES_FOUND")
        return 0

    cleaned_paths: list[str] = []
    for sub in sorted(sub_files):
        p = Path(sub)
        raw = p.read_text(encoding="utf-8", errors="replace")
        cleaned = clean_subtitle_text(raw)
        txt_path = p.with_suffix(".clean.txt")
        txt_path.write_text(cleaned, encoding="utf-8")
        cleaned_paths.append(str(txt_path))

    for cp in cleaned_paths:
        print(f"CLEANED: {cp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
