---
name: composio-automation-catalog
description: "Locate and use a specific archived Composio app-automation skill when an external-app automation is explicitly requested."
---

# Composio Automation Catalog

The Composio library is intentionally archived outside automatic skill discovery
to avoid injecting hundreds of unrelated descriptions into every session. It is
available at `C:\Users\iago.luchtenberg\.codex\skill-library\composio-skills`.

Use this skill only when the task explicitly needs a Composio automation or an
external app covered by that library. Do not load the catalog for ordinary
project work.

1. Search the archive by app or capability, for example with
   `rg --files "C:\\Users\\iago.luchtenberg\\.codex\\skill-library\\composio-skills" | rg -i "slack|calendar"`.
2. Read only the matching `SKILL.md` and follow its instructions.
3. If no matching skill exists, use native Codex tools, an installed connector,
   or clearly report that the catalog has no match. Do not reinstall or expose
   credentials merely to make a skill available.
