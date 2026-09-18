# Contributing

## Development setup

Install `ffmpeg` and make sure `ffmpeg`, `ffprobe`, and `curl` are available.
The script has no third-party Python dependencies.

```bash
cp .env.example .env
chmod 600 .env
python3 -m py_compile openai_srt.py
```

Do not use a real API key or upload real media in automated checks. The CI
workflow only performs a syntax check.

## Pull requests

- Keep changes focused and explain user-visible behavior.
- Never commit `.env`, API keys, media, raw API responses, or generated SRTs.
- Update the README when command-line behavior or prerequisites change.
- Run the local syntax check before opening a pull request.
