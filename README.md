# srt-transcribe

Create English `.srt` subtitles from video or audio using OpenAI's timed
transcription API.

## Features

- Uses `gpt-4o-transcribe-diarize` for timed subtitle segments.
- Speeds audio up to 1.5× by default and restores timestamps to the original
  media timeline.
- Splits long uploads automatically to stay within the timed model's limits.
- Requires no third-party Python packages.
- Keeps API credentials and generated media out of Git.

## Requirements

- Python 3.9 or newer
- `ffmpeg` and `ffprobe`
- `curl`
- An OpenAI API key with access to the transcription API

On macOS:

```bash
brew install ffmpeg
```

The input audio is sent to OpenAI. Do not use this tool for sensitive media
unless that transfer is acceptable for your use case.

## Setup

```bash
git clone https://github.com/magrathean-uk/srt-transcribe.git
cd srt-transcribe
cp .env.example .env
chmod 600 .env
```

Set `OPENAI_API_KEY` in `.env`. Never commit that file.

## Usage

```bash
python3 openai_srt.py /path/to/video.mp4
```

By default, the script creates `/path/to/video.srt` and a compressed MP3 beside
the input. Use an explicit output path when keeping project artifacts together:

```bash
python3 openai_srt.py \
  /Users/bolyki/Downloads/CodexSkillsUpdate.mp4 \
  --output /Users/bolyki/dev/models/srt-transcribe/CodexSkillsUpdate.srt
```

The default `--speed 1.5` reduces upload time and size. Use `--speed 1.0` when
maximum transcription fidelity matters more than upload efficiency. The raw
API response is saved as JSON beside the SRT and is ignored by Git.

OpenAI's upload limit is 25 MB, and the timed model limits an individual
request to 1,400 seconds. The script uses mono 16 kHz 64 kbps MP3 and splits
longer audio into smaller requests automatically.

## Checks

The repository's CI performs a Python syntax check without contacting OpenAI.
Run it locally with:

```bash
python3 -m py_compile openai_srt.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before
opening a change.
