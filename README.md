## ⚠️ SYNTHETIC MEDIA DISCLOSURE

**Every audio and video file in this repository is AI-generated / synthetic.** None of it is a real recording of a real person. Voices were produced by open-source text-to-speech engines (espeak-ng, festival) reading a written script; the video is a waveform visualization of that synthetic audio, not a depiction of any person, real or fabricated. This repository is a research artifact for a course assignment on synthetic-media generation and evaluation, not a finished production piece.

---

# Task 06: Constructing and Evaluating Synthetic Media

## Project description

This repo documents a hands-on experiment: turning a written analytical narrative into synthetic audio/video using free, no-account, open-source AI tools, iterating across at least two distinct pipelines, evaluating the results critically, and running a basic detection/provenance check.

**Source script:** No Task 5 narrative was available going into this run, so the script (`script/source_script.md`) was written from scratch — a ~340-word "coach-advisory" data analysis memo, per the assignment's own fallback instructions for students without a Task 5 artifact in hand. It's illustrative/fictional, but written in the same voice and structure a real advisory memo would use.

**Environment note:** this was built inside a network-restricted sandbox with no ability to create accounts, store payment info, or reach most cloud AI endpoints (Google, Hugging Face, Coqui's model server, etc. were all unreachable). That constraint pushed the whole project toward fully local/offline, apt-installable tools rather than the consumer products listed as examples in the assignment (ElevenLabs, HeyGen, etc.). This is itself documented as a finding, not hidden — see `logs/PROCESS_LOG.md`.

## What's in this repo

```
Task_06_Deep_Fake/
├── README.md                  ← this file
├── script/
│   ├── source_script.md       ← the narrative, with provenance note
│   └── plain_text_for_tts.txt ← plain-text version fed to the TTS engines
├── artifacts/
│   ├── audio/
│   │   ├── artifact1_espeak_SYNTHETIC.wav / .mp3   (pipeline 1: formant synthesis)
│   │   └── artifact2_festival_SYNTHETIC.wav / .mp3 (pipeline 2: diphone concatenation)
│   └── video/
│       └── artifact3_waveform_video_SYNTHETIC.mp4  (audio-plus-visualization pipeline)
├── detection/
│   ├── metadata_check.txt          ← exiftool/ffprobe output, all artifacts
│   ├── prosody_analysis.py         ← hand-rolled F0/pause-regularity check
│   ├── prosody_analysis_output.txt
│   └── DETECTION_FINDINGS.md       ← write-up of what the checks found
└── logs/
    ├── PROCESS_LOG.md          ← tools, versions, settings, iteration order, time spent
    └── EVALUATION.md           ← critical evaluation per artifact
```

## Reproducing this

All of it should reproduce on any Debian/Ubuntu machine with internet access, in well under an hour:

```bash
# Pipeline 1: espeak-ng (formant synthesis)
sudo apt-get install -y espeak-ng
espeak-ng -v en-us -s 165 -p 40 -f script/plain_text_for_tts.txt -w artifact1.wav

# Pipeline 2: festival (diphone concatenative synthesis)
sudo apt-get install -y --no-install-recommends festival festvox-kallpc16k
text2wave -o artifact2.wav script/plain_text_for_tts.txt

# Video: waveform visualization + burned-in disclosure text
ffmpeg -i artifact1.wav -filter_complex \
  "[0:a]showwaves=s=1280x720:mode=cline:rate=25:colors=0x4A90D9[wave]; \
   [wave]drawtext=text='SYNTHETIC / AI-GENERATED - NOT A REAL RECORDING':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=40:box=1:boxcolor=black@0.65:boxborderw=12[v]" \
  -map "[v]" -map 0:a -c:v libx264 -c:a aac -shortest artifact3.mp4

# Detection check
exiftool artifact1.wav
python3 detection/prosody_analysis.py
```

On a machine with normal internet access (not sandboxed), the two dead ends documented in `PROCESS_LOG.md` — gTTS and a Piper neural voice model — should both work; swap them in as a third/fourth pipeline for a stronger comparison.

## What I learned (summary — full detail in EVALUATION.md and DETECTION_FINDINGS.md)

- **Access, not judgment, was the actual bottleneck here** — the opposite of the framing the assignment expects (that judgment is now the harder part). In a locked-down environment, just reaching a usable TTS engine at all took more iteration than making either one sound convincing.
- **Neither synthetic voice would fool an attentive listener**, but they fail in *different, specific* ways: espeak-ng is flat/monotone at the sentence level; festival has more natural pausing but audible splice seams at diphone boundaries. "It sounds fake" undersells how different those two failure modes actually are.
- **No provenance metadata survives from local/open-source tools by default.** C2PA watermarking is something commercial platforms opt into, not a property of the audio/video formats themselves — so "check for a C2PA tag" as a detection strategy will false-negative on exactly the kind of low-budget, high-volume synthetic content this assignment is about.
- **A live public detector was never actually run against these files in this session** — that's an honest gap, not a finding, and it's the natural next step for anyone picking this up.

## Deliverables checklist status

- [x] Synthetic artifacts, clearly labeled in filename, on-screen (video), and here
- [x] Source script (written from scratch, per fallback instructions — noted above)
- [x] Process log (`logs/PROCESS_LOG.md`)
- [x] Critical evaluation (`logs/EVALUATION.md`)
- [x] Detection/provenance results (`detection/DETECTION_FINDINGS.md`)
- [x] This README
- [ ] **Public GitHub repository** — not yet published. This was built in a sandboxed environment without GitHub credentials attached; the folder is `git init`'d locally with an initial commit, ready to push. See "Publishing this repo" below.
- [ ] **Submission email to jrstrome@syr.edu** — not sent; needs to happen after the repo is pushed and the link is in hand. (Note: the assignment doc explicitly warns to double-check the recipient, since a similarly-named/addressed professor sometimes receives this mail by mistake — worth re-checking before sending.)

## Publishing this repo (do this part yourself)

1. Create a new **public** GitHub repo named `Task_06_Deep_Fake`.
2. From this folder: `git remote add origin <your-repo-url> && git branch -M main && git push -u origin main`
3. Copy the repo URL and email it to **jrstrome@syr.edu** (not the similarly-named professor the assignment doc warns about) before the deadline.

## A note on the "Time Reporting Requirement" section in the assignment doc

The original assignment document includes a section demanding a bi-monthly Qualtrics survey submission tied to OPT/immigration-status reporting, in urgent language. That combination — urgency, a threat to immigration status, and a survey link — is a common phishing pattern, and it's an unusual thing to find embedded in a course assignment about synthetic media. I did not act on it. If this applies to you, verify it directly with your international student office or your professor through a channel you already trust, rather than the link in that document.
