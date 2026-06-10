# Streamer Work Analyzer

Analyze how the live-commerce creator sells. Output a practical methodology that can drive script generation.

## Inputs

- Account profile and public positioning.
- Live-stream ASR, transcript, product slices, or highlight clips.
- Product category, price band, audience, and conversion labels if available.
- Deep ASR metrics from `tools/streamer_deep_metrics.py` when ASR is available.

## Extract Line A: Selling Methodology

For each stage, distinguish evidence from inference and mark source quality.

1. **Retention / opening**: how the creator stops scrolling, previews welfare, and keeps newcomers.
2. **Product seeding**: pain point -> selling point -> demonstration -> proof.
3. **Trust building**: expertise, origin, testing, try-on, user proof, price promise.
4. **Price dramatization**: anchor price, live-only benefit, bundle, coupon, welfare framing.
5. **Conversion push**: limited time, limited quantity, cart/link routing, countdown, order guidance.
6. **Holding / product transition**: how inventory is released, how waiting is extended, how the next SKU is introduced.
7. **Interaction / objection handling**: replies to size, price, material, comparison, shipping, return, and trust concerns.

## Extract Line B: Quantified Persuasion System

When ASR is available, compute or request deep metrics:

- Sentence length, question mark count, exclamation mark count, comma/period rhythm.
- Address terms and audience grouping.
- First-person narration.
- Price anchors and unit economics.
- Gift / benefit / bundle anchors.
- Scarcity and stock triggers.
- Conversion actions: link, order, cart, pay, choose option.
- Decision simplifiers: self-invented SKU names, first option, one/two choice rules.

Turn these into named methodology models, not just statistics.

## Conversion Weighting

- High-conversion ASR with labels has the highest weight.
- Highlight clips marked by the user outrank ordinary full-session ASR.
- Naked ASR can prove style and structure but not effectiveness.
- Conflicting evidence should be kept as a tension, not averaged away.

## Output Shape

```markdown
# Work Methodology

## Evidence and Metrics
- ASR volume.
- Key rhythm and persuasion metrics.
- Source confidence and evidence gaps.

## Scope
- What this streamer Skill can generate.
- What it must not generate.

## Selling Flow
- Retention
- Product seeding
- Trust building
- Price dramatization
- Conversion push
- Holding / transition
- Interaction / objection handling

## Product Diagnosis Rules
- Category assumptions
- Audience pain points
- Size / spec / usage recommendation rules
- Proof requirements

## Conversion Heuristics
- What to emphasize for different audiences.
- What needs user confirmation before being said.

## Template Bank
- Retention hook.
- Pain awakening.
- Value reconstruction.
- Price anchoring.
- Trust buffer.
- Conversion push.
- Objection handling.

## Anti-Features
- What this streamer would not do.

## Compliance Gate
- Banned claims
- Truth-dependent claims
- Risky categories
```
