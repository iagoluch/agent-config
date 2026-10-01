# Claude Code — Skill Routing Configuration

## Automatic skill routing

Use `~/.claude/skills/skill-router/SKILL.md` as the first routing reference for technical tasks.

### Rules

- Automatically select relevant skills; do not ask for permission.
- Load only the minimum skills required for the current task.
- Never read all installed `SKILL.md` files just to decide what to do.
- Prefer exact/specific skills over generic ones.
- Project-local instructions always take precedence over global skill instructions.
- Do not mention skill routing unless it materially affects the answer.

### Stack priorities

For this environment, prioritize:

1. Python
2. FastAPI / REST / Pydantic
3. React / TypeScript
4. Git / GitHub
5. SQL / database integration
6. Targeted testing

### Token/validation policy

- Inspect the smallest relevant file set first.
- Do not perform full-repository analysis for a localized request.
- Do not run a full test suite for a localized change unless explicitly requested,
  required by project policy, or a targeted test reveals a broader regression.
- Prefer targeted tests, type checks, linting, or build checks directly related to
  the change.
- Avoid repeating an analysis or test that already established the same fact.
- Escalate validation only when risk or scope justifies it.
- Never sacrifice correctness merely to save tokens.

### Preferred workflow

Request
  -> classify domain
  -> route to specific skill
  -> inspect relevant files
  -> implement
  -> targeted validation
  -> concise report

For cross-stack work:

Backend change -> FastAPI/Python
Frontend change -> React/TypeScript
Database change -> database skill
Repository operation -> Git skill
Behavioral change -> targeted testing

Only combine routes when the task genuinely crosses those boundaries.
