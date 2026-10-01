---
name: contexto
description: Inspect only the minimal Brain context relevant to the current task.
---

# /contexto

Brain lives globally at `~/.claude/brain/` (not inside the current repo). Summarize:
- relevant project memory (`~/.claude/brain/projects/`);
- relevant decisions (`~/.claude/brain/decisions/`);
- current state (`~/.claude/brain/state/current.md`);
- known blockers.

Do not read unrelated Brain files or the entire skill library.
