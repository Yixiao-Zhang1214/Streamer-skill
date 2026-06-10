# Streamer Intake Prompt

Use this intake for Douyin live-commerce creators. The goal is not casual dialogue; the goal is to distill a reusable live-commerce script generator that preserves the creator's public selling persona and method.

## Intake Goal

Collect only the missing information. If the user provides a Douyin profile URL, first parse public fields, echo what was found, and ask the user to confirm or fill gaps.

## Three-Step Funnel

1. **Auto-parse first**: extract public profile fields from a Douyin URL when available.
2. **Compare fields**: separate confirmed, inferred, and missing fields.
3. **Targeted follow-up**: only ask for missing required fields.

## Required Fields

- Creator name / account name.
- Douyin URL or account ID.
- Persona positioning and public profile tags.
- Main product category and price band.
- Target audience / user portrait.
- Past live-stream ASR or transcript material.

## Strongly Recommended Fields

- Conversion or GMV labels by session, product, or segment.
- Highlight clips that the user considers high-converting.
- Product-level ASR slices by SKU.
- Interaction data: comments, questions, live-room Q&A, giveaway timing.
- Selection and pricing mechanism: traffic product, profit product, welfare product.
- Violation, complaint, or risk records.

## Questions To Ask When Missing

1. Who is the creator? Include name, Douyin URL, platform, and public bio if the link cannot be parsed.
2. What should this Skill generate? Example: product scripts, teleprompter scripts, comment replies, short loops, product-card copy.
3. What does the creator sell? Include category, price band, target audience, and forbidden categories.
4. What source material do you have? Provide ASR, product slices, conversion labels, comments, or highlight clips.
5. What compliance constraints apply? Include banned words, sensitive categories, price/stock truth requirements, and platform policy notes.

## Hard Boundaries

- Do not block the workflow if profile parsing fails. Fall back to manual fields.
- Do not infer private personality from a performance persona.
- Do not treat naked ASR as proof of high conversion unless conversion labels are provided.
- Do not store full transcripts in the final Skill; use structured summaries and short phrase-level markers only.
