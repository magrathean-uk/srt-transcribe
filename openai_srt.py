#!/usr/bin/env python3
"""Create an English SRT from media using OpenAI's timed transcription API."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


API_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_MODEL = "gpt-4o-transcribe-diarize"
MAX_UPLOAD_BYTES = 25_000_000
MAX_MODEL_SECONDS = 1_400.0
CHUNK_SECONDS = 1_300.0


def parse_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values


def get_api_key(env_file: Path) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = parse_dotenv(env_file).get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            f"Missing OPENAI_API_KEY. Set it in {env_file} or in the environment."
        )
    return api_key


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Required command not found: {name}")


def speed_label(speed: float) -> str:
    return f"{speed:g}"


def extract_audio(input_path: Path, audio_path: Path, speed: float) -> None:
    audio_path.parent.mkdir(parents=True, exist_ok=True)
    if audio_path.exists() and audio_path.stat().st_size > 0:
        print(f"Reusing audio: {audio_path}")
        return

    print(f"Extracting {speed:g}x mono 16 kHz MP3: {audio_path}")
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-filter:a",
        f"atempo={speed:g}",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "64k",
        str(audio_path),
    ]
    subprocess.run(command, check=True)


def probe_duration(audio_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def split_audio(audio_path: Path, directory: Path) -> list[Path]:
    pattern = directory / "chunk-%03d.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(audio_path),
            "-map",
            "0:a:0",
            "-f",
            "segment",
            "-segment_time",
            str(int(CHUNK_SECONDS)),
            "-reset_timestamps",
            "1",
            "-c:a",
            "libmp3lame",
            "-b:a",
            "64k",
            str(pattern),
        ],
        check=True,
    )
    chunks = sorted(directory.glob("chunk-*.mp3"))
    if not chunks:
        raise SystemExit(f"Could not split audio into API-sized chunks: {audio_path}")
    return chunks


def transcribe(audio_path: Path, api_key: str, model: str) -> dict:
    if audio_path.stat().st_size > MAX_UPLOAD_BYTES:
        size_mb = audio_path.stat().st_size / 1_000_000
        raise SystemExit(
            f"Audio is {size_mb:.1f} MB; the OpenAI upload limit is 25 MB. "
            "Use a higher speed or lower bitrate."
        )

    curl_command = [
        "curl",
        "--fail-with-body",
        "--silent",
        "--show-error",
        "--connect-timeout",
        "30",
        "--max-time",
        "1800",
        "--request",
        "POST",
        "--url",
        API_URL,
        "--form",
        f"model={model}",
        "--form",
        f"file=@{audio_path};type=audio/mpeg",
        "--form",
        "response_format=diarized_json",
        "--form",
        "chunking_strategy=auto",
        "--form",
        "language=en",
        "--config",
        "-",
    ]
    curl_config = f'header = "Authorization: Bearer {api_key}"\n'
    result = subprocess.run(
        curl_command,
        input=curl_config,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        error = "\n".join(
            part.strip() for part in (result.stdout, result.stderr) if part.strip()
        )
        error = error.replace(api_key, "[REDACTED]")
        raise SystemExit(f"OpenAI transcription failed:\n{error[-4000:]}")

    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"OpenAI returned invalid JSON: {exc}") from exc
    if "error" in response:
        raise SystemExit(f"OpenAI transcription failed: {response['error']}")
    if not response.get("segments"):
        raise SystemExit("OpenAI returned no timed segments.")
    return response


def transcribe_with_chunking(audio_path: Path, api_key: str, model: str) -> dict:
    duration = probe_duration(audio_path)
    if duration <= MAX_MODEL_SECONDS:
        return transcribe(audio_path, api_key, model)

    print(
        f"Audio is {duration:.1f}s; splitting into {CHUNK_SECONDS:.0f}s API chunks."
    )
    with tempfile.TemporaryDirectory(prefix="openai-srt-") as temp_dir:
        chunks = split_audio(audio_path, Path(temp_dir))
        combined: dict = {
            "model": model,
            "segments": [],
            "chunks": [],
        }
        offset = 0.0
        for index, chunk in enumerate(chunks, start=1):
            chunk_duration = probe_duration(chunk)
            print(
                f"Uploading chunk {index}/{len(chunks)} "
                f"({chunk_duration:.1f}s, {chunk.stat().st_size / 1_000_000:.1f} MB)..."
            )
            response = transcribe(chunk, api_key, model)
            for segment in response["segments"]:
                adjusted = dict(segment)
                adjusted["start"] = float(segment["start"]) + offset
                adjusted["end"] = float(segment["end"]) + offset
                combined["segments"].append(adjusted)
            combined["chunks"].append(
                {
                    "file": chunk.name,
                    "duration": chunk_duration,
                    "segment_count": len(response["segments"]),
                }
            )
            offset += chunk_duration
        combined["text"] = " ".join(
            str(segment.get("text", "")).strip()
            for segment in combined["segments"]
            if str(segment.get("text", "")).strip()
        )
        return combined


def format_timestamp(seconds: float) -> str:
    total_milliseconds = max(0, round(seconds * 1000))
    hours, remainder = divmod(total_milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_part, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d},{milliseconds:03d}"


def wrap_subtitle(text: str, width: int = 42) -> str:
    words = " ".join(text.split()).split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return "\n".join(lines)


def write_srt(response: dict, output_path: Path, speed: float) -> int:
    blocks: list[str] = []
    for segment in response["segments"]:
        text = str(segment.get("text", "")).strip()
        if not text:
            continue
        start = float(segment["start"]) * speed
        end = float(segment["end"]) * speed
        if end <= start:
            continue
        blocks.append(
            f"{len(blocks) + 1}\n"
            f"{format_timestamp(start)} --> {format_timestamp(end)}\n"
            f"{wrap_subtitle(text)}"
        )

    if not blocks:
        raise SystemExit("OpenAI returned no usable subtitle segments.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    return len(blocks)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract audio and create an English SRT with OpenAI."
    )
    parser.add_argument("input", type=Path, help="Video or audio file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="SRT output path (default: next to input)",
    )
    parser.add_argument(
        "--audio",
        type=Path,
        help="Compressed audio path (default: next to input)",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        help="dotenv file (default: .env next to this script)",
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.5,
        help="Audio speed before upload; timestamps are restored (default: 1.5)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Timed OpenAI model (default: {DEFAULT_MODEL})",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    input_path = args.input.expanduser().resolve()
    if not input_path.is_file():
        raise SystemExit(f"Input file not found: {input_path}")
    if not 0.5 <= args.speed <= 2.0:
        raise SystemExit("--speed must be between 0.5 and 2.0 for ffmpeg atempo.")

    script_dir = Path(__file__).resolve().parent
    env_file = (args.env_file or script_dir / ".env").expanduser().resolve()
    output_path = (
        args.output.expanduser().resolve()
        if args.output
        else input_path.with_suffix(".srt")
    )
    audio_path = (
        args.audio.expanduser().resolve()
        if args.audio
        else input_path.with_name(
            f"{input_path.stem}.openai-{speed_label(args.speed)}x.mp3"
        )
    )
    raw_path = output_path.with_suffix(".json")

    require_tool("ffmpeg")
    require_tool("ffprobe")
    require_tool("curl")
    api_key = get_api_key(env_file)
    extract_audio(input_path, audio_path, args.speed)
    print(f"Uploading {audio_path.stat().st_size / 1_000_000:.1f} MB to OpenAI...")
    response = transcribe_with_chunking(audio_path, api_key, args.model)
    raw_path.write_text(json.dumps(response, indent=2) + "\n", encoding="utf-8")
    segment_count = write_srt(response, output_path, args.speed)
    print(f"Wrote {segment_count} subtitles: {output_path}")
    print(f"Saved API response: {raw_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
