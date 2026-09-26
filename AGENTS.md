# Repository guidance

## Scope

`openai_srt.py` contains the CLI, audio conversion, API requests, chunking,
and SRT formatting. It uses the Python standard library and invokes
`ffmpeg`, `ffprobe`, and `curl`. Keep changes focused and preserve unrelated
work. Do not add Python dependencies without a concrete need.

## Behavior to preserve

- Environment `OPENAI_API_KEY` takes precedence over the selected dotenv file.
  Keep keys out of command-line arguments, logs, fixtures, and commits.
- API requests upload media and may incur charges. Use synthetic data and
  mocked responses for local checks; use live uploads only when authorized.
- Chunk offsets are measured on the extracted audio timeline before SRT
  timestamps are multiplied by `--speed`.
- Existing nonempty MP3 files are reused. SRT and JSON destinations are
  overwritten. Changes to these behaviors need explicit documentation.
- Keep generated audio, subtitles, API responses, and private media out of
  contributions. Git ignore patterns do not protect files outside this repo.
- Preserve the full MIT license and contributor copyright notice. Follow
  [SECURITY.md](SECURITY.md) for vulnerability reports.

## Validation

The existing CI command is `python -m py_compile openai_srt.py` on Python
3.12. Locally, use `python3 -m py_compile openai_srt.py`; this writes bytecode
and checks syntax only. Inspect options with `python3 openai_srt.py --help`.
There is no automated behavioral test suite.

For behavior changes, validate the affected path using synthetic fixtures or
mocked subprocess/API results. Check speed scaling and chunk offsets for
timing changes, credential precedence for configuration changes, and file
reuse and output paths for file-handling changes. Report what was actually
checked and any remaining live-service or media-quality gap.

Update [README.md](README.md) when options, defaults, output paths, or
requirements change. See [CONTRIBUTING.md](CONTRIBUTING.md) for review
expectations. Complete authorized changes through their relevant checks,
including safe local edits, Git work, and necessary setup implied by the task.
Honor explicit exclusions without asking again for permission already given.
Use bounded delegation for independent work when it is useful; keep file
ownership distinct. Ask only when a consequential action falls outside the
authorized scope.

## Optional tooling

Consider [Clean Development](https://github.com/magrathean-uk/clean-development)
when managing development caches across projects.
