"""
Lightweight, dependency-minimal 'detector' used as our provenance/detection check
(assignment option: 'ask ... whether the transcript reads as AI-generated' /
academic-tool-style check). This is NOT a trained deepfake classifier -- it's a
simple signal-processing pass that looks at two things forensic audio checks
commonly flag in synthetic speech: pitch (F0) variance and pause regularity.
Real human speech tends to have more irregular, less metronomic pausing and
wider pitch excursions than rule-based/concatenative TTS.

Uses only numpy + scipy (already available), no network access required.
"""
import numpy as np
import wave
import sys

def load_wav(path):
    with wave.open(path, 'rb') as w:
        sr = w.getframerate()
        n = w.getnframes()
        raw = w.readframes(n)
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
        if w.getnchannels() > 1:
            data = data.reshape(-1, w.getnchannels()).mean(axis=1)
        return data / 32768.0, sr

def frame_signal(sig, sr, frame_ms=40, hop_ms=20):
    frame_len = int(sr * frame_ms / 1000)
    hop_len = int(sr * hop_ms / 1000)
    frames = []
    for start in range(0, len(sig) - frame_len, hop_len):
        frames.append(sig[start:start + frame_len])
    return np.array(frames)

def estimate_f0_autocorr(frame, sr, fmin=75, fmax=400):
    frame = frame - np.mean(frame)
    if np.max(np.abs(frame)) < 1e-4:
        return 0.0
    corr = np.correlate(frame, frame, mode='full')
    corr = corr[len(corr)//2:]
    min_lag = int(sr / fmax)
    max_lag = int(sr / fmin)
    if max_lag >= len(corr):
        return 0.0
    segment = corr[min_lag:max_lag]
    if len(segment) == 0 or np.max(segment) <= 0:
        return 0.0
    peak = np.argmax(segment) + min_lag
    if corr[0] == 0:
        return 0.0
    if segment[np.argmax(segment)] / (corr[0] + 1e-9) < 0.3:
        return 0.0  # unvoiced / silence, low periodicity confidence
    return sr / peak

def analyze(path, label):
    sig, sr = load_wav(path)
    frames = frame_signal(sig, sr)
    energies = np.sqrt(np.mean(frames ** 2, axis=1))
    voiced_thresh = np.percentile(energies, 40)
    f0s = []
    silence_flags = []
    for f, e in zip(frames, energies):
        silence_flags.append(e < voiced_thresh)
        if e >= voiced_thresh:
            f0 = estimate_f0_autocorr(f, sr)
            if f0 > 0:
                f0s.append(f0)
    f0s = np.array(f0s)

    # pause-length statistics: run-lengths of consecutive "silent" frames
    silence_flags = np.array(silence_flags)
    pause_lengths = []
    run = 0
    for s in silence_flags:
        if s:
            run += 1
        else:
            if run > 0:
                pause_lengths.append(run)
            run = 0
    if run > 0:
        pause_lengths.append(run)
    pause_lengths = np.array(pause_lengths) if pause_lengths else np.array([0])

    result = {
        "label": label,
        "path": path,
        "duration_sec": round(len(sig) / sr, 2),
        "n_voiced_frames": int(len(f0s)),
        "f0_mean_hz": round(float(np.mean(f0s)), 1) if len(f0s) else None,
        "f0_std_hz": round(float(np.std(f0s)), 1) if len(f0s) else None,
        "f0_cv_percent": round(float(np.std(f0s) / np.mean(f0s) * 100), 1) if len(f0s) and np.mean(f0s) > 0 else None,
        "n_pauses": int(len(pause_lengths)),
        "pause_len_mean_frames": round(float(np.mean(pause_lengths)), 2),
        "pause_len_std_frames": round(float(np.std(pause_lengths)), 2),
        "pause_len_cv_percent": round(float(np.std(pause_lengths) / np.mean(pause_lengths) * 100), 1) if np.mean(pause_lengths) > 0 else None,
    }
    return result

if __name__ == "__main__":
    targets = [
        ("artifacts/audio/artifact1_espeak_SYNTHETIC.wav", "espeak-ng (formant synthesis)"),
        ("artifacts/audio/artifact2_festival_SYNTHETIC.wav", "festival (diphone concatenative)"),
    ]
    print(f"{'metric':30s} | {'espeak-ng':>18s} | {'festival':>18s}")
    print("-" * 72)
    results = [analyze(p, l) for p, l in targets]
    keys = ["duration_sec", "f0_mean_hz", "f0_std_hz", "f0_cv_percent",
            "n_pauses", "pause_len_mean_frames", "pause_len_std_frames", "pause_len_cv_percent"]
    for k in keys:
        print(f"{k:30s} | {str(results[0][k]):>18s} | {str(results[1][k]):>18s}")
