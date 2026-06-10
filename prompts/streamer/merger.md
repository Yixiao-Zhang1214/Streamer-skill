# Streamer Merger Prompt

Use this prompt when updating an existing streamer Skill with new sessions, ASR, conversion labels, product categories, or compliance rules.

## Update Classification

Classify each new piece of material as one or more of:

- Persona expression change.
- Live-room flow change.
- Product/category method change.
- Conversion evidence update.
- Audience relationship update.
- Compliance or risk update.

## Merge Rules

- Update the smallest relevant section only.
- Preserve time sensitivity; live-commerce style changes quickly, so mark important changes with dates when available.
- Do not promote one-off event copy into a core rule unless repeated or high-conversion evidence supports it.
- If evidence conflicts, keep the conflict and explain likely context.
- Add risky or non-compliant patterns to boundaries, not to reusable tactics.

## Output

Produce patches for `work.md` and/or `persona.md`, plus a short note on evidence quality and remaining gaps.
