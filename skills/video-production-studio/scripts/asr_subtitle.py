"""Transcribe audio/video to SRT subtitles locally using faster-whisper (CUDA auto-detect)."""

from __future__ import annotations

import argparse
from pathlib import Path

from faster_whisper import WhisperModel


def fmt_ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def load_model(model_size: str, device: str) -> tuple[WhisperModel, str]:
    if device == "auto":
        try:
            import ctranslate2
            if ctranslate2.get_cuda_device_count() > 0:
                return WhisperModel(model_size, device="cuda", compute_type="float16"), "cuda/float16"
        except Exception:
            pass
        return WhisperModel(model_size, device="cpu", compute_type="int8"), "cpu/int8"
    ctype = "float16" if device == "cuda" else "int8"
    return WhisperModel(model_size, device=device, compute_type=ctype), f"{device}/{ctype}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SRT subtitles with faster-whisper.")
    parser.add_argument("input", help="Path to audio or video file")
    parser.add_argument("--out", default="", help="Output SRT path (default: <input>.srt)")
    parser.add_argument("--model", default="small", help="Whisper model size: tiny/base/small/medium/large-v3")
    parser.add_argument("--lang", default="zh", help="Language code (e.g. zh, en, ja, or auto)")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    args = parser.parse_args()

    src = Path(args.input).resolve()
    out_srt = Path(args.out).resolve() if args.out else src.with_suffix(".srt")

    model, mode = load_model(args.model, args.device)
    lang = None if args.lang == "auto" else args.lang
    segments, info = model.transcribe(str(src), language=lang, vad_filter=True)

    lines: list[str] = []
    count = 0
    for idx, seg in enumerate(segments, start=1):
        txt = seg.text.strip()
        if not txt:
            continue
        count += 1
        lines.append(f"{count}\n{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}\n{txt}\n")

    out_srt.parent.mkdir(parents=True, exist_ok=True)
    out_srt.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK_SRT: {out_srt} (segments={count}, lang={info.language}, mode={mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
