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
  [SECURITY.md](.github/SECURITY.md) for vulnerability reports.
- Legal files (`LICENSE`, `NOTICE`, `docs/legal/`, contributor terms,
  copyright and attribution strings) are owner-controlled: change them only
  on the owner's explicit instruction.

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
requirements change. See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for review
expectations. Complete authorized changes through their relevant checks,
including safe local edits, Git work, and necessary setup implied by the task.
Honor explicit exclusions without asking again for permission already given.
Use bounded delegation for independent work when it is useful; keep file
ownership distinct. Ask only when a consequential action falls outside the
authorized scope.

<!-- clean-development-policy:v2 (canonical text: ~/dev/source/dev-bootstrap/snippets/clean-development-policy.md) -->
## Clean development (mandatory)

This project follows [Clean Development](https://github.com/magrathean-uk/clean-development) and the machine rule that nothing creates tool state under `~` (only the allow-listed agent homes).

- Load `~/dev/machine/env.zsh`; `~/.zshenv` does this for every zsh. Machine storage preferences live in `~/dev/machine/storage.conf`; workspace navigation is in `~/dev/START-HERE.md`.
- New sessions select `/Volumes/4TB/machine/cache` when the configured volume is actually mounted and writable, otherwise `~/dev/machine/cache` for ordinary smaller work. Use routed `DEVCACHE`, `CLEAN_DEVELOPMENT_{ROOT,CACHE_ROOT,BUILD_ROOT,SCRATCH_ROOT}`, `BOLYKI_DEV_LIBS` and `TMPDIR`; builds and scratch are beneath the selected cache. Keep active-session destinations fixed; stop if required storage disappears. Other users configure their own volume and fallback.
- SpecieX, large video/model jobs and VMs require external storage; never use internal fallback. Persistent labs, credentials, installed toolchains, source and final deliverables are not disposable caches.
- All active Git entry points belong under `~/dev/source/`, third-party repositories in `source/third-party/`, websites in `source/magrathean/`, and Teslatlas products/docs in `source/teslatlas-service/`. Do not read, scan, move or edit `~/dev/porn`.
- Preserve routed tool homes/caches, caller overrides and SDK/toolchain choices. Never unset or bypass routing. Scrubbed environments must restore the reviewed routing before cache-writing tools run; preserve intentional hermetic Git/Cargo isolation.
- Run builds, tests, installs and anything else that writes caches or build output through Clean Development: `clean-development run --session session-only -- <command>`. Follow its docs and keep its receipts.
- Do not add installers or scripts that default into `~` (`~/.cargo`, `~/.rustup`, `~/.cache`, `~/.npm`, `~/.swiftpm`, `~/.gradle`, ...) and do not hardcode `$HOME` paths for caches; use the routed variables.
- Before finishing, run `dev-env-check`, `dev-projects-check` and `dev-audit`; require passing environment/project checks and no new home-audit entries compared with the task baseline. Fix violations your work caused.
