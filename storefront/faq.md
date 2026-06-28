# FAQ

## Does this modify my DeepSeek CLI?

No. The overlay floats above your terminal. It reads from a FIFO pipe.
Your CLI runs normally underneath.

## How is this different from just screen-translating?

It's deterministic — translations are cached and replayable. It captures
the full conversation with thinking traces, not just OCR'd snippets.
It also translates your English prompts back to Chinese.

## Does it need an API key?

No. The CLI output translator uses Google Translate for free (no key).
The bidirectional prompt translator defaults to your local LM Studio or
Ollama instance. Google Translate is the emergency fallback.

## Can I replay a session?

Yes. Every session is saved to `~/.cli-overlay/state-{id}.json`. Run
`python3 replay.py ~/.cli-overlay/state-*.json` to replay it into the overlay.

## Can I export training data?

Yes. `python3 scripts/export_training_trace.py state.json --out trace.jsonl`
produces ML-ready JSONL with structured tags.

## What does PASS mean?

PASS means no blocking issues were detected under configured checks.
PASS does not mean the artifact is secure, vulnerability-free, or safe
to execute without review. Translation accuracy varies by engine.

## Which claims are forbidden?

- This artifact is safe.
- This code is secure.
- No vulnerabilities exist.
- No hidden attack exists.
- This package is safe to execute without further review.
- PASS guarantees safety.
