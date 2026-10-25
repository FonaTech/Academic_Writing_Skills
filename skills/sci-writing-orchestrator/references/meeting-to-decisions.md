# From meeting recordings and supervisor comments to decisions

## Transcription (offline)
Whisper through Hugging Face `transformers` runs locally on Apple Silicon (MPS):

```bash
python3 scripts/transcribe_meeting.py "Review第三次手稿meeting.m4a" --model openai/whisper-small --lang zh --out meeting.txt
```

- `whisper-tiny` is fast and enough to capture decisions; `whisper-small` or larger reduces errors in technical terms.
- Audio is decoded with ffmpeg, cut into 30 s chunks and transcribed in batches; the script collapses the repetition loops that small models produce in silence ("对对对…").
- Long silences and off-topic parts are kept with timestamps but not interpreted.

## Extraction
Read the transcript for decisions, not dialogue. Record each item as:

| Time | Speaker (if known) | Decision or request | Applies to | Action |
|---|---|---|---|---|
| 11:00 | supervisor | applications should explain which property of the subject is used and what function it enables | Section 6 | adopt as the application micro-structure |
| 58:00 | supervisor | differential pairs are first a way to represent negative weights; common-mode rejection is secondary | Section 4.3 | reorder the section |

Typical content of group meetings: structural decisions, emphasis ("the review is about this subject, not the neighbouring field"), technical corrections (why a standard parameter choice is used), references to read, and deadlines.

## Rules
- Quote nothing from a low-quality transcript in the manuscript; use it only to decide what to write.
- If a decision is ambiguous, ask the user in one short question and propose the likely reading.
- Keep the decision table in the writing plan so later agents follow it.
