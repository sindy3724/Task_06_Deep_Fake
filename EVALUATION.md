# Critical Evaluation

Honest assessment of each artifact against the assignment's evaluation questions: where it holds up, where it fails, whether it would fool a casual viewer, and what got blocked or degraded.

## Artifact 1 — `artifact1_espeak_SYNTHETIC.wav` (espeak-ng, formant synthesis)

**Where it holds up:** Word-level intelligibility is genuinely good — every word in the transcript is recoverable on first listen, including domain jargon like "acute-to-chronic workload ratio." Timing/pacing through numbers (620, eighteen percent, 1.5) is clean; it doesn't stumble on digits the way some TTS does.

**Where it fails:** This is the one nobody would mistake for a person. The intonation is close to monotone at the sentence level — F0 varies within words (see detection findings) but doesn't do the larger rise-fall shaping a real coach would use to land the three recommendations as three separate, weighted points. There's no breath, no micro-pause before the emphatic "and this is the one I'd push hardest on," and every sentence ends on roughly the same falling contour regardless of whether it's a statement or an instruction. It reads more like a screen reader than a person talking to a colleague.

**Would it fool a casual viewer?** No — within the first two seconds. This is the classic "obviously synthetic" register, useful precisely because it's a clean baseline to compare the other artifacts against.

**Refusals / degradation:** None. espeak-ng is a fully local, unfiltered formant synthesizer — there's no safety layer to trigger. Worth naming as its own finding: the least "product-like" tool was also the only one with zero content moderation of any kind.

## Artifact 2 — `artifact2_festival_SYNTHETIC.wav` (festival, diphone concatenative synthesis)

**Where it holds up:** Noticeably more natural phrasing than espeak-ng — the pause-length analysis backs this up numerically (higher pause-length variability, CV 131.9% vs 93.2%). Sentence-final falls sound less clipped, and short function words ("it's," "that's") blend into the surrounding words the way connected human speech does, which is exactly what diphone concatenation is designed to do well.

**Where it fails:** Concatenation seams are audible at some diphone boundaries, especially around less common consonant clusters — you can hear where two recorded fragments were spliced rather than one continuous vocal gesture. The voice also doesn't vary pace with content; a fast, punchy clause like "None of this requires benching anyone" gets the same measured pace as a hedged aside, so it under-delivers the rhetorical emphasis a real coach would put there.

**Would it fool a casual viewer?** Probably not on close listening, but on a quick scroll-by with other audio/background noise present, this is closer to "maybe a low-quality recording" than "definitely a robot" — a meaningfully different failure mode than artifact 1.

**Refusals / degradation:** None triggered — same story as espeak-ng, no filter layer.

## Artifact 3 — `artifact3_waveform_video_SYNTHETIC.mp4` (audio-plus-visualization pipeline)

This is the "video" deliverable, built as an audio-plus-image/waveform pipeline rather than a face/lip-sync pipeline — a deliberate choice: doing this without any commercial account meant no access to a talking-head tool, and using a generic waveform visualization sidesteps the assignment's likeness/consent constraint entirely (no face, real or synthetic, is depicted).

**Where it holds up:** The disclosure text is burned directly into the frame (not just in the filename/README), which is closer to true "on-screen disclosure" than most consumer tools bother with by default. The waveform itself is an honest visual — it's literally a rendering of the actual audio signal, so nothing about the visual track is fabricated or could mislead about what's shown.

**Where it fails:** As a piece of "synthetic media" in the deepfake sense, this barely counts — there's no synthetic visual content depicting a person, which is both the safest choice and the least ambitious one relative to what the assignment describes (HeyGen/D-ID/Wav2Lip-style talking heads). This is the artifact where the gap between "what I produced" and "what a polished result looks like" is largest, and that gap is itself the most useful data point in this whole log: the actual barrier to a convincing talking-head deepfake, in this run, was tool/account access, not technical difficulty — which matches the assignment's framing that "the barrier is no longer access; it is judgment," except in this specific case access genuinely was the constraint, and it's worth being honest that judgment wasn't even the thing being tested here.

**Would it fool a casual viewer?** N/A in the deepfake sense — nobody would mistake a labeled waveform video for a real recording of a person, which was the point.

## Summary across artifacts

| | espeak-ng | festival | waveform video |
|---|---|---|---|
| Fools a casual listener/viewer? | No | Maybe, briefly | N/A (no face) |
| Biggest tell | Flat sentence-level intonation | Audible concatenation seams | Not attempting a face at all |
| Setup effort | ~5 min (apt install) | ~5 min (apt install) | ~15 min (ffmpeg filter graph) |
| Cost | $0 | $0 | $0 |

The two voice pipelines land in the same place as most "genuinely free, no account, no internet-dependent" synthetic voice options: intelligible, unmistakably synthetic, and each with a distinct failure signature (monotone vs. spliced) rather than one being strictly "better." Neither is close to fooling anyone who is listening for it, which is a real answer to the assignment's research question about effort — for these tools, "convincing enough to fool a casual scroller" was not reached within a single afternoon at $0 spend, and the limiting factor was tool capability, not iteration count.
