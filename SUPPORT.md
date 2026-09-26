# Support

Use [GitHub issues](https://github.com/magrathean-uk/srt-transcribe/issues)
for usage questions, reproducible bugs, and feature requests. For
vulnerabilities or exposed credentials, follow [SECURITY.md](SECURITY.md).

## Common problems

| Symptom | Check |
| --- | --- |
| `Required command not found` | Put `ffmpeg`, `ffprobe`, and `curl` on `PATH`. |
| `Missing OPENAI_API_KEY` | Set the environment variable or edit the dotenv file beside the script. Use `--env-file` for another location. |
| `Input file not found` | Supply an existing video or audio file. |
| Speed rejected | Use a value from `0.5` through `2.0`. |
| Error saving JSON | Create the parent directory of `--output` before running. |
| Unexpected transcript after changing input or speed | Use a fresh `--audio` path; nonempty MP3 files are reused without validation. |
| OpenAI request failed | Review the sanitized error, key access, selected model, and service availability. The script does not retry. |
| No timed or usable segments | Check that the model accepts the requested format and that the audio contains intelligible English speech. |
| Audio rejected as too large | A short reused MP3 may exceed the byte limit without triggering duration-based splitting. Use a fresh audio path to extract the input at the script's encoding settings. |

## Reporting a bug

Include the revision, operating system, Python and external-tool versions,
the command with private paths removed, expected behavior, and the error.
Mention whether the MP3 was freshly extracted or reused, the speed, and
whether the recording was chunked.

Prefer a small synthetic example. Do not post API keys, dotenv contents,
private recordings, transcripts, or raw API responses. Inspect logs before
sharing them; automatic key redaction is not a general privacy filter.
