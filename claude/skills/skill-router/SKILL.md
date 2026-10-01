---
name: skill-router
description: Route tasks to the smallest relevant set of installed skills using the current project state and available Claude Brain context. Optimized for Python, FastAPI, React, TypeScript, Git, databases, APIs, testing, browser verification, documents, and external-app integrations.
---

# Skill Router + Brain

## Before work

1. Read only the relevant project state/memory.
2. Classify the task by domain, complexity, and risk.
3. Select the smallest relevant skill set.
4. Add secondary skills only when the task genuinely crosses domains.

Do not recursively inspect the entire skill library.

## Skill discovery

Claude Code discovers skills normally when each skill is exposed as:

`~/.claude/skills/<skill-name>/SKILL.md`

This package contains nested source collections (`composio-skills` and `document-skills`).
`configure-skills.bat` creates top-level directory junctions to those source folders,
so the same skill files remain single-source and are still discoverable by Claude Code.

Do not read every `SKILL.md` to build a catalog. Use the skill descriptions surfaced by
Claude Code and open the selected skill only when needed.

## Routing

- Feature/change -> `incremental-implementation`
- API/interface -> `api-and-interface-design`
- React/TypeScript/UI -> `frontend-ui-engineering`
- Bug/debugging -> `debugging-and-error-recovery`
- Tests -> `test-driven-development`
- Code review -> `code-review-and-quality`
- Simplification/refactor -> `code-simplification`
- Security -> `security-and-hardening`
- Performance -> `performance-optimization`
- Git/branches/commits/PRs -> `git-workflow-and-versioning`
- CI/CD -> `ci-cd-and-automation`
- Documentation/ADR -> `documentation-and-adrs`
- Observability -> `observability-and-instrumentation`
- Specifications -> `spec-driven-development`
- Planning -> `planning-and-task-breakdown`
- Official-doc verification -> `source-driven-development`
- Browser/runtime verification -> `browser-testing-with-devtools` / `webapp-testing`
- PDF/DOCX/PPTX/XLSX -> the corresponding document skill
- External-app actions -> `connect` / `connect-apps` or the specific integration skill
- Other domains -> select the most specific installed skill by its description

For cross-stack tasks, combine only the affected domains.

## Brain use

Treat brain files as context, not authority over the code.

Trust order:
1. Current code and project files
2. Explicit user instructions
3. Project `CLAUDE.md` / rules
4. Brain decisions and project memory
5. General skill guidance
6. Inference

When memory conflicts with current code, current code wins and the mismatch may be recorded as a pending correction.

## Effort control

### Tiny / localized
Direct fix; minimal context; targeted validation.

### Normal
Inspect affected files; use the primary skill; run directly relevant checks.

### Complex / risky
Investigate dependencies and cross-domain impact; combine skills; broaden validation only when justified.

Do not increase effort merely because many files exist.

## Delegation

Use one primary implementation agent when a task can be owned coherently by one agent.

Use multiple agents only for genuinely independent workstreams, such as parallel evidence gathering,
review, testing, or isolated domain work.

Never duplicate the same investigation across model tiers.

## Validation

- Tiny/localized -> direct targeted validation.
- Normal -> relevant tests/checks and contract verification.
- Complex/risky -> relevant tests plus regression analysis and broader checks where justified.

Do not run a full suite by default.

## Completion

After meaningful changes:
- verify the requested behavior;
- ensure relevant consumers/contracts remain coherent;
- understand the working-tree state;
- record only durable knowledge;
- report only material changes, issues, validation, and limitations.

