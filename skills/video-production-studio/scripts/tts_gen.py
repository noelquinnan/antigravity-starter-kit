"""Generate narration MP3 and synchronized SRT subtitles using edge-tts."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

import edge_tts


async def synthesize(text: str, voice: str, rate: str, out_audio: Path, out_srt: Path | None) -> None:
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    submaker = edge_tts.SubMaker()
    out_audio.parent.mkdir(parents=True, exist_ok=True)

    with out_audio.open("wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in {"WordBoundary", "SentenceBoundary"}:
                submaker.feed(chunk)

    if out_srt is not None:
        out_srt.parent.mkdir(parents=True, exist_ok=True)
        out_srt.write_text(submaker.get_srt(), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate TTS audio and SRT via edge-tts.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Direct narration text")
    group.add_argument("--text-file", help="Path to UTF-8 text file")
    parser.add_argument("--voice", default="zh-CN-XiaoxiaoNeural", help="Edge TTS voice name")
    parser.add_argument("--rate", default="+0%", help="Speech rate, e.g. +10% or -5%")
    parser.add_argument("--out-audio", required=True, help="Output MP3 file path")
    parser.add_argument("--out-srt", default="", help="Optional output SRT subtitle path")
    args = parser.parse_args()

    text = args.text if args.text is not None else Path(args.text_file).read_text(encoding="utf-8")
    out_audio = Path(args.out_audio).resolve()
    out_srt = Path(args.out_srt).resolve() if args.out_srt else out_audio.with_suffix(".srt")

    asyncio.run(synthesize(text.strip(), args.voice, args.rate, out_audio, out_srt))
    print(f"OK_AUDIO: {out_audio}")
    print(f"OK_SRT:   {out_srt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
