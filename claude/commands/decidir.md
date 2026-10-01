---
name: decidir
description: Record an explicit technical or architectural decision in Brain.
---

# /decidir

Brain lives globally at `~/.claude/brain/` (not inside the current repo). When the user provides or asks to formalize a decision, create a dated file in
`~/.claude/brain/decisions/` with:
- Status
- Context
- Decision
- Alternatives
- Impact

Do not record unconfirmed hypotheses as decisions.
