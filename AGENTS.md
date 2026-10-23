# srt-transcribe project context

`openai_srt.py` contains the CLI, audio conversion, API requests, chunking and SRT formatting. It uses the Python standard library and invokes `ffmpeg`, `ffprobe` and `curl`.

## Runtime behaviour

- Environment variable `OPENAI_API_KEY` takes precedence over the selected dotenv file.
- API requests upload media and may incur charges.
- Chunk offsets are measured on the extracted audio timeline before SRT timestamps are multiplied by `--speed`.
- Existing non-empty MP3 files are reused. SRT and JSON destinations are overwritten.
- Generated artefacts include audio, subtitles and API responses.

## Command and documentation references

The existing CI command is `python -m py_compile openai_srt.py` on Python 3.12. Local syntax and help commands are:

```bash
python3 -m py_compile openai_srt.py
python3 openai_srt.py --help
```

Compilation writes bytecode and checks syntax. There is no automated behavioural test suite. Synthetic fixtures and mocked subprocess or API results support local checks of timing, credential precedence, file reuse and output paths. Live-service and media-quality checks exercise additional behaviour.

[README.md](README.md) describes options, defaults, output paths and requirements. [CONTRIBUTING.md](.github/CONTRIBUTING.md) describes review practices, and [SECURITY.md](.github/SECURITY.md) describes vulnerability reporting. The project carries the MIT licence and contributor copyright notice.
