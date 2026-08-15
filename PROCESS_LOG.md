# Process Log

Running log of tools, versions, prompts/settings, iteration order, what broke, and rough time spent. Session run 2026-08-15, in a network-restricted Linux sandbox (no GUI, no ability to sign up for accounts or store payment info) — that constraint shaped almost every tool choice below, and is itself part of the finding.

## 0. Source script (~10 min)

No Task 5 narrative was available, so wrote a ~340-word "coach-advisory" script from scratch per the assignment's fallback instructions (see `script/source_script.md`). Chose a sports-analytics workload-management memo because it's the exact example genre the assignment names, and because a data-driven advisory register (specific numbers, hedged recommendations, direct address to "Coach") gives the TTS engines real prosodic work to do — much more diagnostic than reading generic prose.

## 1. Environment check (~10 min)

Checked what was already installed: `ffmpeg` present, `git` present, no `gh` CLI (no authenticated GitHub access from this sandbox — see Deliverables note in README). No TTS libraries preinstalled.

Tried the two obvious "free tier" paths first:
- **gTTS** (`pip install gTTS`) — installs fine, but calling it failed: `ProxyError ... Tunnel connection failed: 403 Forbidden` against `translate.google.com`. The sandbox's network egress is allow-listed to package registries (PyPI) and a narrow set of hosts; general internet endpoints like Google's translate backend are blocked. **This is a real free-tier constraint, just not the kind the assignment expected** — the blocker wasn't a paywall, it was sandbox network policy.
- Checked reachability of other common model hosts: `huggingface.co`, `storage.googleapis.com`, `models.silero.ai`, `coqui.gateway.scarf.sh` — all unreachable (connection refused/timed out). `github.com` (direct release-asset downloads) and `pypi.org` *were* reachable.

Given that, pivoted to **fully offline, apt-installable** TTS engines for the two required distinct pipelines, plus one extra attempt at a higher-quality neural option using what github access was available.

## 2. Pipeline 1 — espeak-ng (~10 min)

- Installed via `apt-get install espeak-ng` (version 1.51, Debian package `1.51+dfsg-12build1`).
- Command: `espeak-ng -v en-us -s 165 -p 40 -f script/plain_text_for_tts.txt -w artifact1_espeak_SYNTHETIC.wav`
- Settings: voice `en-us`, speed 165 wpm, pitch 40 (default-ish, slightly below default 50 for a lower register).
- Worked first try. Output: 1:58, 22.05kHz mono WAV, ~5.2MB. Converted to MP3 (qscale 4) for a smaller companion file.
- **Failure mode surfaced immediately on listen:** flat sentence-level intonation, screen-reader cadence. See EVALUATION.md.

## 3. Pipeline 2 — festival (~15 min, one real failure)

- First install attempt (`apt-get install festival festvox-kallpc16k`) **failed**: a transitive dependency (`libatopology2t64` from `security.ubuntu.com`) 404'd. Classic "the mirror and the index are out of sync" apt failure, not something specific to festival.
- Fix: `apt-get update` then retried with `--no-install-recommends` to drop the unrelated `alsa-utils` dependency chain that was pulling in the broken package. Second attempt succeeded (festival 2.5.0-10, festvox-kallpc16k 2.4-1 voice data).
- Command: `text2wave -o artifact2_festival_SYNTHETIC.wav script/plain_text_for_tts.txt`
- No settings exposed beyond the default `kal` diphone voice (didn't dig into festival's Scheme config for this pass — flagged as a follow-up in Bonus Challenges territory).
- Worked on retry. Output: 2:13, 16kHz mono WAV, ~4.3MB — noticeably more natural pausing than espeak-ng on listen; also confirmed numerically (pause-length CV 131.9% vs 93.2%, see DETECTION_FINDINGS.md).

## 4. Attempted bonus pipeline — local neural TTS (~20 min, did not complete)

Tried to get a genuinely neural, locally-run voice (the assignment's own bonus-challenge bar) working without a cloud account:

- `pip install TTS` (Coqui) was avoided once its model-download host (`coqui.gateway.scarf.sh`) tested unreachable.
- Tried **Piper** instead: the `piper` binary itself downloaded fine from a GitHub release (`rhasspy/piper` releases, direct asset URL reachable). But the voice model files (`.onnx`, hosted in the separate `rhasspy/piper-voices` repo, which is backed by Hugging Face LFS storage even when accessed through github.com) came back `403 Forbidden` — `"GitHub access to this repository is not enabled for this session."` The sandbox's GitHub access is repo-allow-listed, and `piper-voices` wasn't on the list.
- **Stopped here rather than burn more time working around a sandbox permission boundary.** Documenting this as a deliberate incomplete attempt: the binary and the pipeline design were both viable, the blocker was purely "which specific repos/hosts this environment can reach," which is exactly the kind of free-tier/access constraint the assignment wants documented, even though in this case the constraint is about the *research environment*, not the *AI tool's own* free tier.

## 5. Video artifact — audio + waveform visualization (~15 min)

- No account-based face/video tool (HeyGen, D-ID, Synthesia, Wav2Lip needing a face image) was usable without either an account or a source likeness. Rather than fabricate a face, built a video pipeline entirely from the audio: `ffmpeg`'s `showwaves` filter renders the actual waveform, with `drawtext` burning in a synthetic-media disclosure banner and a footer crediting the voice engine.
- One filter-graph iteration: first pass had disclosure text sized/positioned fine at 1280x720; kept those settings for the final render.
- Output: `artifact3_waveform_video_SYNTHETIC.mp4`, 1:58 (matches the espeak-ng audio it's built from), H.264/AAC, ~19MB.
- This is a legitimate but modest reading of "video if feasible" — see EVALUATION.md for why this was the honest choice given constraints rather than attempting a face pipeline with no consented likeness available.

## 6. Detection / provenance check (~20 min)

- `exiftool` + `ffprobe` metadata dump on all three artifacts: confirmed no C2PA manifest, no watermark tag, on any of them.
- Wrote `detection/prosody_analysis.py` (numpy/scipy only, no network) to compare F0 variance and pause-length regularity between the two audio pipelines as a stand-in for a trained detector.
- Searched for a free, no-login public audio deepfake detector to actually run the artifacts through. Found several candidates (eyesift.com, undetectable.ai, deepfakecheck.io). Attempted to drive one via browser automation; the browser bridge was not connected in this session, so the live-detector step was **not completed** — documented as an open gap rather than skipped silently. See DETECTION_FINDINGS.md.

## 7. Documentation (~20 min)

Wrote EVALUATION.md, DETECTION_FINDINGS.md, this log, and README.md.

## Rough time-in-hours summary

| Step | Time |
|---|---|
| Script writing | ~10 min |
| Environment / network probing | ~10 min |
| espeak-ng pipeline | ~10 min |
| festival pipeline (incl. one apt failure) | ~15 min |
| Piper/neural-TTS attempt (incomplete) | ~20 min |
| Video (waveform) pipeline | ~15 min |
| Detection/provenance check | ~20 min |
| Documentation | ~20 min |
| **Total** | **~2 hours** |

Cost in tool credits: $0 across every step — everything used was either preinstalled, apt-installable, or a public GitHub release binary.
