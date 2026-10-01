---
name: status
description: Show a compact operational status of the current project and Brain.
---

# /status

Brain lives globally at `~/.claude/brain/` (not inside the current repo). Read only:
- `~/.claude/brain/state/current.md`
- the matching `~/.claude/brain/projects/*.md` file when present
- the most recent relevant decision file

Also inspect `git status --short` and the current branch if available.

Return:
- project;
- branch;
- changed files;
- current known blockers;
- next explicit step.

Do not run the full test suite.
