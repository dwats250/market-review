# Handoffs

A tiny channel between the two assistants. `chatgpt-latest.md` is ChatGPT's latest note to Claude; `claude-latest.md` is Claude's latest note to ChatGPT.

Rules:

- Each latest file is at most two short paragraphs.
- Replace it when there is something material to pass; do not build a history. Durable material belongs in `daily/`, `weekly/`, `discussions/`, `hypotheses.md` or `gaps.md`.
- Handoffs are context, never authority or evidence.
- They may contain product/process vitals, notable findings, unresolved risks, and the current working market question.
- If an assistant is doing an independent market read, it must form that read from evidence BEFORE reading the other assistant's handoff. This preserves the existing independence rule.
- Owner instructions and canonical repo documents always win.
