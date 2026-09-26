# Security Policy

## Scope and support

This policy covers the tracked Python command-line tool and its local
configuration examples. Only the latest code on `main` is supported, with no
separate versioned release support table. Include the branch and commit you tested when reporting a problem.

## Reporting a vulnerability

Report vulnerabilities privately using the email route published in the
[Magrathean UK security policy](https://raw.githubusercontent.com/magrathean-uk/.github/main/SECURITY.md):
`contact@magrathean.uk`, with the subject `SECURITY: srt-transcribe`.
Do not put vulnerability details in public issues, discussions, or pull requests.

GitHub private vulnerability reporting is currently disabled for this
repository. Use the organization email route above.

Include the affected revision, a minimal reproduction, expected and actual
behavior, and impact. Remove credentials and personal data from supporting
evidence. Do not send private media or raw API responses containing sensitive
data.

If an OpenAI API key may be exposed, revoke it through the OpenAI account that
issued it before reporting the incident.

## Security boundaries

- The script reads `OPENAI_API_KEY` from the environment or a local dotenv
  file. Keep dotenv files local and out of commits.
- Audio from the selected media is converted locally and uploaded to OpenAI's
  transcription endpoint. The resulting transcript may contain information
  from that media.
- The script writes an SRT file, a JSON API response, and normally a compressed
  audio file to paths chosen from the input or command-line options. Review
  those locations before sharing or committing their contents.
- `ffmpeg`, `ffprobe`, and `curl` run locally with the permissions of the user
  who starts the command. Their security and update policies are outside this
  repository.

The script redacts the literal API key from one API-error path. Treat all logs
and generated files as potentially sensitive and review them before sharing.

## Reportable issues

Report issues that could expose an API key, media, transcript, or API response;
send data to an unintended destination; or let untrusted input cause unsafe
local behavior. A vulnerability in an external tool or service can also matter
when this tool's integration makes the impact material.

This policy is reporting guidance, not a security audit or a promise of a
response time.
