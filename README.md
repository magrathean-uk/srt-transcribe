<h1 align="center">srt-transcribe</h1>

<p align="center">Turns English speech in a video or audio file into an SRT subtitle file using OpenAI transcription.</p>

<p align="center">
  <a href="docs/index.md">Documentation</a> ·
  <a href="docs/legal/privacy.md">Privacy</a>
</p>

## Overview

srt-transcribe extracts mono 16 kHz MP3 audio locally with FFmpeg, uploads it to OpenAI, and converts the timed segments it returns into subtitles. By default it speeds the audio up to 1.5× and scales the subtitle timestamps back to the original timeline. It requests English transcription, not translation, and speaker labels returned by the API are not included in the SRT. This is a single Python script with no third-party Python packages.

## Features

- Single Python script with no third-party Python packages.
- Extracts and compresses audio locally with FFmpeg before uploading.
- Speeds audio up by default and rescales subtitle timestamps to match.
- Splits long recordings into chunks automatically.
- Requests English transcription, not translation.

## Getting started

### Requirements

- Python 3.11 or newer. The existing CI checks syntax on Python 3.12 only.
- `ffmpeg` with `libmp3lame` and `atempo`, plus `ffprobe`, on your `PATH`.
- `curl` with support for `--fail-with-body`.
- An OpenAI API key with access to the selected transcription model.

Audio is uploaded to OpenAI. MP3, JSON, and SRT files remain on your computer.
Choose media you are permitted to send to that service. See
[Security](.github/SECURITY.md) and [Privacy](docs/legal/privacy.md) for the
reporting policy and data-handling details.

### Setup

```bash
git clone https://github.com/magrathean-uk/srt-transcribe.git
cd srt-transcribe
cp .env.example .env
chmod 600 .env
```

For a new checkout, edit `.env` and set `OPENAI_API_KEY`. If you already have
that file, edit it instead of copying over it. You can also supply the key
through the `OPENAI_API_KEY` environment variable, which takes precedence
over the file. The default `.env` location is beside `openai_srt.py`, even
when you run the script from another directory.

### Create subtitles

From the checkout directory:

```bash
python3 openai_srt.py /path/to/video.mp4
```

For that example, the default outputs are:

| File | Contents |
| --- | --- |
| `/path/to/video.srt` | Subtitles on the original media timeline |
| `/path/to/video.openai-1.5x.mp3` | Compressed audio used for upload |
| `/path/to/video.json` | API response, or combined responses for chunked audio |

The JSON path is the SRT output path with its suffix replaced by `.json`.
Existing SRT and JSON files at those paths are overwritten. A nonempty MP3
at the selected audio path is reused without checking its input or speed.
Use a new audio path when changing the input or speed, especially if you
supply `--audio` explicitly.

To keep all outputs in one directory, create it first and set both paths:

```bash
mkdir -p output
python3 openai_srt.py /path/to/video.mp4 \
  --output output/video.srt \
  --audio output/video.openai-1.5x.mp3
```

`--output` alone does not move the MP3. Its parent directory must exist when
the JSON response is written. Use `--speed 1.0` to transcribe without
speeding up the audio, then review the subtitles against the original media.
Transcription accuracy and synchronization are not guaranteed.

### Command reference

```bash
python3 openai_srt.py --help
```

| Argument | Meaning | Default |
| --- | --- | --- |
| `input` | Video or audio file | Required |
| `-o`, `--output` | SRT destination | Input path with `.srt` suffix |
| `--audio` | MP3 destination or existing MP3 to reuse | `<input-stem>.openai-<speed>x.mp3` beside input |
| `--env-file` | File containing `OPENAI_API_KEY` | `.env` beside the script |
| `--speed` | Audio speed from `0.5` through `2.0` | `1.5` |
| `--model` | Model used for timed transcription | `gpt-4o-transcribe-diarize` |

A model override must accept `response_format=diarized_json`,
`chunking_strategy=auto`, and `language=en`, and return timed `segments`.
Changing the model name does not change the request format.

### Long recordings and output details

The script checks the duration of the extracted MP3. Above its configured
1,400-second threshold, it splits the audio into approximately 1,300-second
chunks and uploads them sequentially. It rejects any individual upload
larger than 25,000,000 bytes. Splitting is triggered by duration, not file
size; an oversized reused MP3 can therefore fail without being split.
These are the script's configured limits, not a guarantee of current API
availability or limits.

Temporary chunks are cleaned up when the temporary-directory context exits.
The extracted MP3, JSON response, and SRT remain. There is no retry or resume
mechanism, and rerunning uploads the audio again, even when the MP3 is reused.

JSON segment times refer to the sped-up audio timeline; the SRT multiplies
them by `--speed`. For chunked audio, JSON combines adjusted segments and
chunk metadata rather than preserving each complete response. Subtitle text
wraps at word boundaries with a target width of 42 characters, without a
fixed two-line limit.

## Documentation

- [Licensing and third-party tools](docs/licensing.md)
- [Privacy](docs/legal/privacy.md)

## Help and development

See [Support](.github/SUPPORT.md) for common errors and what to include in a
bug report. For changes, read [Contributing](.github/CONTRIBUTING.md) and the
[Code of Conduct](.github/CODE_OF_CONDUCT.md). Report vulnerabilities through
[Security](.github/SECURITY.md).

The existing CI runs a Python syntax check:

```bash
python3 -m py_compile openai_srt.py
```

This creates local bytecode and does not test FFmpeg, API access, subtitle
quality, or synchronization. No automated behavioral test suite is included.

## Licence

srt-transcribe is open source under the MIT licence. See [LICENSE](LICENSE).
Contributions: see [CONTRIBUTING](.github/CONTRIBUTING.md).

<sub>© 2026 srt-transcribe contributors · [Legal](https://github.com/magrathean-uk/.github/blob/main/LEGAL.md)</sub>
