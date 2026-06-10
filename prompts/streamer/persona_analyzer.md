# Streamer Persona Analyzer

Analyze the creator's public live-room persona. The target is a performance system, not private personality.

## Extract Line B: Persona

1. **Expression style**: catchphrases, address terms, rhythm, filler words, sentence length, intensity changes.
2. **Emotional curve**: calm seeding, rising urgency, climax push, cool-down, recovery after doubt or cold room.
3. **Memory points**: signature moves, fixed jokes, assistant/control-room coordination, recurring proof gestures.
4. **Boundaries and taboos**: categories not sold, claims not made, tone not used, identity lines not crossed.

## Quantified Persona Signals

When ASR is available, use `tools/streamer_deep_metrics.py` or equivalent metrics to ground the persona:

- Average and median sentence length.
- Question mark and exclamation mark density.
- Address-term counts.
- First-person count and "I recommend / I calculate" posture.
- Price, gift, stock, and conversion-action counts.
- Decision-simplification phrases and self-invented SKU naming.

Do not leave these as raw numbers only. Explain what each metric implies about the live-room persona.

## Live-Room Relationship

- How the creator names and groups the audience.
- How they create intimacy without overclaiming personal relationship.
- How they answer praise, doubt, bargaining, size/spec questions, and complaints.
- How they switch between friend, expert, shop owner, tester, and welfare giver.

## Evidence Rules

- Translate vague labels into executable speech patterns.
- Use short phrase-level markers only; do not paste long transcript blocks.
- Mark what is supported by ASR, profile, comments, conversion data, or user inference.
- Keep the boundary between public persona and private self explicit.

## Output Shape

```markdown
# Persona Analysis

## Layer 0: Core Performance Rules
## Layer 1: Streamer Context
## Layer 2: Expression DNA
## Layer 3: Signature Phrases
## Layer 4: Thinking Models
## Layer 5: Emotional Curve
## Layer 6: Audience Relationship
## Layer 7: Commercial Persona
## Layer 8: Anti-Features
## Layer 9: Boundaries and Risks
```
