---
id: 9
title: "Shell command batching rule needs a structural guard"
status: open
type: open-source
skill: [task-observer]
proposes_skill: []
target_file: []
siblings_checked: "none — no skill-families.md registry exists in this workspace"
area: "structural enforcement after a loaded command-execution rule is violated"
date: 2026-10-01
session_context: "A validation tool call chained independent Python compile, pytest and git diff checks with PowerShell separators even though the active execution rules required independent calls or Promise batching."
parked_until: ""
resolved: ""
resolution: ""
reference: ""
---

**Issue:** A clearly loaded rule against chaining shell commands was still violated during final validation. The written instruction alone did not prevent the command shape.

**Suggested improvement:** Add a pre-dispatch check to task-observer or the command orchestration layer that detects independent commands joined by shell separators and requires separate parallel tool calls before execution.

**Principle:** Repeatedly important command-shape constraints need a structural preflight, because prose awareness does not reliably constrain the final tool payload.