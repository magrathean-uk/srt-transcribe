# srt-transcribe

Turn English speech in a video or audio file into an SRT subtitle file using
OpenAI transcription. This is a single Python script with no third-party
Python packages.

The script extracts mono 16 kHz MP3 audio with FFmpeg, uploads it to OpenAI,
and converts timed segments into subtitles. By default it speeds the audio
up to 1.5× and scales the subtitle timestamps back to the original timeline.
It requests English transcription, not translation. Speaker labels returned
by the API are not included in the SRT.

## Requirements

- Python 3.9 or newer. The existing CI checks syntax on Python 3.12 only.
- `ffmpeg` with `libmp3lame` and `atempo`, plus `ffprobe`, on your `PATH`.
- `curl` with support for `--fail-with-body`.
- An OpenAI API key with access to the selected transcription model.

Audio is uploaded to OpenAI. MP3, JSON, and SRT files remain on your computer.
Choose media you are permitted to send to that service. See
[Security and privacy](SECURITY.md) for the data-handling boundaries.

## Setup

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

## Create subtitles

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

## Command reference

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

## Long recordings and output details

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

## Help and development

See [Support](SUPPORT.md) for common errors and what to include in a bug
report. For changes, read [Contributing](CONTRIBUTING.md) and the
[Code of Conduct](CODE_OF_CONDUCT.md).

The existing CI runs a Python syntax check:

```bash
python3 -m py_compile openai_srt.py
```

This creates local bytecode and does not test FFmpeg, API access, subtitle
quality, or synchronization. No automated behavioral test suite is included.

## License

Released under the [MIT License](LICENSE), copyright © 2026 srt-transcribe
contributors. See [Licensing and third-party tools](docs/licensing.md) for
the distinction between this script, its external tools, and the media you
process.
