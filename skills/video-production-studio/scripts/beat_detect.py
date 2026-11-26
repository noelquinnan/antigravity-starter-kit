"""Detect BPM, beat timestamps, and strong onset peaks from audio or video."""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import librosa
import numpy as np


def ensure_wav(src: Path, tmp_dir: Path) -> Path:
    if src.suffix.lower() in {".wav", ".mp3", ".flac", ".ogg"}:
        return src
    wav = tmp_dir / "extracted.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src), "-ac", "1", "-ar", "22050", str(wav)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return wav


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze BPM and beat/onset timestamps.")
    parser.add_argument("input", help="Path to audio or video file")
    parser.add_argument("--out", default="", help="Optional output JSON path")
    parser.add_argument("--start", type=float, default=0.0, help="Start offset in seconds")
    parser.add_argument("--duration", type=float, default=None, help="Duration in seconds")
    args = parser.parse_args()

    src = Path(args.input).resolve()
    with tempfile.TemporaryDirectory() as td:
        audio_path = ensure_wav(src, Path(td))
        y, sr = librosa.load(str(audio_path), sr=22050, offset=args.start, duration=args.duration)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])
    beats_sec = [round(float(t) + args.start, 3) for t in librosa.frames_to_time(beat_frames, sr=sr)]

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env, sr=sr, backtrack=False, delta=0.25, wait=8
    )
    strong_sec = [round(float(t) + args.start, 3) for t in librosa.frames_to_time(onset_frames, sr=sr)]

    result = {
        "source": str(src),
        "bpm": round(bpm, 2),
        "beat_count": len(beats_sec),
        "beats_sec": beats_sec,
        "beats_ms": [int(round(t * 1000)) for t in beats_sec],
        "strong_onsets_sec": strong_sec,
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
        print(f"SAVED: {out_path} (BPM={result['bpm']}, beats={result['beat_count']}, onsets={len(strong_sec)})")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
