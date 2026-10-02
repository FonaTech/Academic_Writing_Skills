#!/usr/bin/env python3
"""Transcribe a meeting recording offline with Whisper (Hugging Face transformers).

Usage
  transcribe_meeting.py AUDIO [--model openai/whisper-small] [--lang zh] [--out meeting.txt]
                        [--chunk 30] [--batch 16] [--start 0] [--duration 0]

Requires ffmpeg on PATH and the Python packages transformers, torch and numpy. Runs on
Apple Silicon (MPS), CUDA or CPU. Output lines are "[mm:ss] text"; repetition loops that
small models produce on silence are collapsed. The transcript is for extracting decisions
(see references/meeting-to-decisions.md), not for quotation.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys


def load_audio(path, start=0.0, duration=0.0, rate=16000):
    import numpy as np
    cmd = ['ffmpeg', '-v', 'error']
    if start:
        cmd += ['-ss', str(start)]
    if duration:
        cmd += ['-t', str(duration)]
    cmd += ['-i', path, '-ac', '1', '-ar', str(rate), '-f', 'f32le', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32)


def collapse(text: str) -> str:
    text = re.sub(r'(.{1,6}?)\1{4,}', r'\1…', text)          # 对对对对… → 对…
    text = re.sub(r'((?:\S+\s){1,4}\S+)(?:\s\1){2,}', r'\1 …', text)
    return text.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('audio')
    ap.add_argument('--model', default='openai/whisper-small')
    ap.add_argument('--lang', default='zh')
    ap.add_argument('--out', default='')
    ap.add_argument('--chunk', type=int, default=30)
    ap.add_argument('--batch', type=int, default=16)
    ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--duration', type=float, default=0.0)
    args = ap.parse_args(argv)

    import torch
    from transformers import pipeline
    device = 'mps' if torch.backends.mps.is_available() else ('cuda:0' if torch.cuda.is_available() else 'cpu')
    asr = pipeline('automatic-speech-recognition', model=args.model, device=device)
    audio = load_audio(args.audio, args.start, args.duration)
    step = args.chunk * 16000
    chunks = [audio[i:i + step] for i in range(0, len(audio), step)]
    out = open(args.out, 'w', encoding='utf-8') if args.out else sys.stdout
    for i in range(0, len(chunks), args.batch):
        batch = [{'raw': c, 'sampling_rate': 16000} for c in chunks[i:i + args.batch]]
        results = asr(batch, batch_size=args.batch,
                      generate_kwargs={'language': args.lang, 'task': 'transcribe'})
        for j, r in enumerate(results):
            t = int(args.start) + (i + j) * args.chunk
            out.write(f'[{t // 60:02d}:{t % 60:02d}] {collapse(r["text"])}\n')
            out.flush()
    if args.out:
        out.close()
        print(f'wrote {args.out} ({len(chunks)} chunks of {args.chunk} s, model {args.model}, device {device})')


if __name__ == '__main__':
    main()
