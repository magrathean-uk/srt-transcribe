# Security Policy

## Supported version

Only the latest code on the `main` branch is supported.

## Reporting a vulnerability

Please do not open a public issue for a security vulnerability, leaked
credential, privacy problem, or unsafe handling of media.

Use GitHub's private vulnerability reporting or a private message to the
repository owner. Include the affected revision, reproduction steps, impact,
and any relevant logs with secrets and personal data removed.

If an OpenAI key may have been exposed, revoke it immediately in the OpenAI
dashboard before reporting the incident.

## Security boundaries

- `.env` is local-only and must never be committed.
- The tool sends selected audio to OpenAI for transcription; do not process
  sensitive media unless that transfer is acceptable for your use case.
- `ffmpeg`, `ffprobe`, and `curl` run locally with the permissions of the user
  who starts the script.
- Generated audio, subtitles, API responses, and comparison logs are ignored
  by Git by default.
