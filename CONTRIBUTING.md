# Contributing

## Before opening a pull request

Keep each change focused. Update `README.md` when command-line behavior,
prerequisites, or data handling changes. Read `SECURITY.md` before reporting a
security or privacy concern.

The repository's documented local check is:

```bash
python3 -m py_compile openai_srt.py
```

Do not use a real API key or upload real media in automated checks. The tracked
CI workflow performs only the Python syntax check.

## Sensitive and generated files

Never commit dotenv files, API keys, media, raw API responses, generated audio,
subtitles, or logs that contain private data. Review the paths selected by
`--output`, `--audio`, and `--env-file` before running the command.

## Rights and licensing

The repository is licensed under the MIT License. Read
[`docs/licensing.md`](docs/licensing.md) and the root [`LICENSE`](LICENSE)
before contributing.

This repository does not contain a contributor license agreement, DCO, or
copyright-assignment policy. Do not submit code, media, text, or other material
unless you have the right to contribute it. For third-party material or a
contribution that needs terms beyond the MIT License, ask a maintainer to state
the applicable terms before proceeding.

## Pull requests

Describe the user-visible behavior and the check you ran. Do not use a pull
request or public issue to disclose a security vulnerability, credential,
private media, or raw API response.
