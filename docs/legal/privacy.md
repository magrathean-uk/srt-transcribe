# Privacy

srt-transcribe extracts audio locally, then uploads it to OpenAI so you get a transcript back; nothing else leaves your device.

Last updated 27 September 2026

## What leaves your device

The media file you select is never uploaded as-is. srt-transcribe extracts its audio locally with FFmpeg, compresses it to mono 16 kHz MP3, and uploads that compressed audio to OpenAI's transcription API for speech-to-text. The resulting transcript may contain information from the original media.

## What srt-transcribe reads

The script reads your `OPENAI_API_KEY` from the environment or a local dotenv file beside it.

## What srt-transcribe writes locally

Each run normally writes three files to paths chosen from your input file or command-line options: an SRT subtitle file, a JSON API response, and the compressed audio file used for upload. All three can contain information from your source media. Treat them as sensitive, and review them before sharing or committing their contents.

## Your responsibility

Only choose media you are permitted to send to OpenAI. srt-transcribe does not check permissions, ownership, or consent on your behalf.
