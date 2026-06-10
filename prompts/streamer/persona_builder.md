# Streamer Persona Builder

Build `persona.md` for a Douyin live-commerce creator. Focus on the public selling persona and live-room performance system, not private personality.

The output must be a deep research-grade persona model, comparable to or stronger than the `livestream-host-zhouzhou` reference style: quantified, evidence-aware, reusable, and operational for script generation.

## Minimum Depth Standard

- Target length: roughly 180-260 lines unless source material is genuinely too thin.
- Include quantitative ASR metrics when available: sentence length, question marks, exclamation marks, first-person count, address terms, price anchors, gift signals, scarcity signals, conversion actions, and decision-simplification signals.
- Include a `Signature Phrases` table with phrase, function, and evidence/frequency.
- Include 5-8 thinking / selling models, not just surface tone.
- Include "不像她的表达 / anti-features" so generation knows what to avoid.
- Keep evidence boundaries explicit: public live-room persona only, no private personality inference.
- Use short phrase-level markers only; never paste long transcript blocks.

## Required Structure

```markdown
# {creator_name} - Streamer Persona

## Layer 0: Core Performance Rules
- The creator's persona rules that always override copywriting convenience.
- How to respond to doubt, cold room, repeated questions, and conversion moments.
- What must never be imitated or claimed.

## Layer 1: Streamer Context
- Platform: Douyin or other platform.
- Product vertical.
- Price band.
- Audience nickname and target audience.
- Main generation use cases.

## Layer 2: Expression DNA
- Address terms.
- Catchphrases.
- Rhythm and sentence style.
- Repeated proof gestures.
- Short sample patterns, not long transcript quotes.

## Layer 3: Signature Phrases
- Table: phrase / function / source or frequency.
- Include address terms, price anchors, gift anchors, scarcity triggers, conversion actions, and decision simplifiers.

## Layer 4: Thinking Models
- Value reconstruction model.
- Price anchoring model.
- Decision simplification model.
- Question-rhythm interaction model.
- Conversion loop model.
- Scarcity model.
- Trust and risk-buffering model.

## Layer 5: Emotional Curve
- Opening energy.
- Product explanation energy.
- Trust-building energy.
- Conversion peak.
- Cool-down and transition.

## Layer 6: Audience Relationship
- How to create intimacy.
- How to answer questions.
- How to handle doubts and comparison.
- How to preserve trust while selling.

## Layer 7: Commercial Persona
- Expert / shop owner / tester / friend roles.
- What role is used in each stage of the selling flow.
- How persona supports conversion without fake claims.

## Layer 8: Anti-Features
- What would not sound like this streamer.
- Long generic brand storytelling vs live-room conversion rhythm.
- Over-soft seeding without price/gift/action.
- Unsafe absolute claims.

## Layer 9: Risks and Honest Boundaries
- Performance persona vs private personality.
- Evidence gaps.
- Compliance risks.
- Claims that require user confirmation.

## Correction Log
(empty)
```
