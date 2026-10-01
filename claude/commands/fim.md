---
name: fim
description: Consolidate the current session into durable Brain memory without recording noise.
---

# /fim

Review the current session's work and repository state.

Update Brain only when there is durable knowledge:
- new decision;
- architecture change;
- stable convention;
- significant bug/root cause;
- meaningful project state;
- explicit next step.

Brain lives globally at `~/.claude/brain/` (not inside the current repo). Write:
- decisions to `~/.claude/brain/decisions/`;
- project state to `~/.claude/brain/projects/`;
- concise session metadata to `~/.claude/brain/sessions/`.

Do not store chat filler, temporary thoughts, or details that can be trivially rediscovered from code.

At the end, report exactly what memory files were changed.
