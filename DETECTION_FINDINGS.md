# Detection / Provenance Check

**Artifacts checked:** `artifact1_espeak_SYNTHETIC.wav`, `artifact2_festival_SYNTHETIC.wav` (see `prosody_analysis.py` for methodology), plus metadata checks on all three artifacts including the video.

## 1. Metadata / watermark / C2PA check

Ran `exiftool` and `ffprobe` against every artifact (full output in `metadata_check.txt`). Finding: **none of the three artifacts carry any C2PA content-credential manifest, digital watermark, or synthetic-media tag of any kind.** `espeak-ng`, `festival`, and plain `ffmpeg` muxing simply do not write provenance metadata — that's a feature of commercial platforms (e.g. some OpenAI, Google, and Adobe tools embed C2PA manifests by default), not of the underlying audio/video containers themselves. This is a meaningful finding on its own: **the free, local, open-source path is the path with the least built-in provenance signal.** A downstream viewer who only checks "does this file have a C2PA manifest?" would get a false negative for AI-generated content produced this way — the absence of a watermark says nothing about whether content is synthetic, only about which tool made it.

## 2. Algorithmic prosody check (stand-in for an academic/forensic detector)

Public ML-based deepfake-audio detectors (Hive, Deepware, etc.) were not reachable from this sandboxed environment (see note below), so as a substitute I wrote a small, dependency-light script (`prosody_analysis.py`, numpy + scipy only) that measures two things forensic audio analysis commonly looks at in synthetic speech:

- **F0 (pitch) variance** — human pitch tends to wander more; some rule-based TTS is comparatively monotone.
- **Pause-length regularity** — human pausing is irregular (breath, hesitation, emphasis); some synthesis paces pauses on a near-fixed clock.

Results:

| metric | espeak-ng | festival |
|---|---|---|
| duration (s) | 118.08 | 133.18 |
| F0 mean (Hz) | 103.4 | 115.4 |
| F0 std (Hz) | 53.9 | 55.9 |
| F0 coefficient of variation (%) | 52.1 | 48.5 |
| pause count | 445 | 441 |
| pause length mean (frames) | 5.31 | 6.04 |
| pause length std (frames) | 4.94 | 7.97 |
| pause length CV (%) | 93.2 | 131.9 |

**Interpretation:** both engines actually show fairly high pitch variance (~50% CV) — higher than I expected going in, which is itself a finding: naive "monotone pitch = robotic" heuristics don't cleanly separate these two synthetic sources from each other, let alone from human speech, without a real reference recording to compare against. Festival's pause-length CV (131.9%) is notably higher than espeak-ng's (93.2%), consistent with festival's diphone/prosody model inserting more variable-length pauses at phrase boundaries, versus espeak-ng's more rule-driven, evenly-spaced pausing. That tracked with what I heard by ear: festival's cadence sounds less metronomic. This is a weak, hand-rolled signal, not a validated classifier — see limitations below.

## 3. Attempted live public detector (browser)

I attempted to reach a free, no-login web-based audio deepfake detector (candidates found via search: eyesift.com/audio-analysis, undetectable.ai/ai-voice-detector, deepfakecheck.io) to upload the artifacts directly. The browser-automation bridge was not connected in this session, so the upload step could not be completed here. **If you're picking this repo up on your own machine, this is the step to run yourself**: upload `artifact1_espeak_SYNTHETIC.wav` (or the video) to one of the links above and record the confidence score and whether the tool explains its reasoning — then append the result to this file. That's a genuine gap in this run's coverage, and it's worth being upfront about rather than skipping the step silently.

## Limitations of this check

- The prosody script is a heuristic I wrote for this assignment, not a trained/validated deepfake classifier. It should not be read as "these results prove X is AI or not" — it's evidence in the same category as "the voice sounded a little flat to me," just made numeric and reproducible.
- No comparison against a real human recording of the same script was done in this pass (see Bonus Challenges — recording yourself reading the script and comparing is the natural follow-up).
- A real public detector was not actually run against the artifacts in this session; only attempted. That's an honest failure to document, not a result to report as success.
