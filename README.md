# agent-config (PRIVADO)

Backup/portabilidade das configurações de **Claude Code** (`claude/`) e **Codex** (`codex/`).
Gerado em 2026-10-01. **Nunca tornar público**: contém memória e skills do projeto Gestor de Peças.

## Conteúdo
- `claude/` — CLAUDE.md, settings.json, agents, commands, hooks, skills (junctions já resolvidas), brain, memory (por projeto), skill-observations, plugins (só manifestos).
- `codex/` — AGENTS.md, config.toml, hooks.json, agents, hooks, rules, skills, skill-library, automations, memories.

## Fora do repo de propósito
`.credentials.json`, `auth.json`, `.claude.json`, bancos sqlite, sessões/transcripts, caches de plugins, `skills-quarentena-*`.
`codex/config.toml`: o header `Authorization` do MCP `omniroute` foi trocado por `<REDACTED>` — recoloque na máquina nova.

## Instalar em outra máquina
- Codex: copie `codex/*` para `~/.codex/` (faça backup antes). Ajuste os caminhos absolutos de Windows (`C:\Users\iago.luchtenberg\...`) em `config.toml` e `hooks.json`; reinstale os plugins/marketplaces listados em `config.toml`.
- Claude: copie `claude/*` para `~/.claude/` (memória: `claude/memory/<pasta-do-projeto>` → `~/.claude/projects/<pasta-do-projeto>/memory`). Ajuste caminhos em `settings.json` e `hooks/`; rode `/plugin` para reinstalar `pg@aiguide`, `superpowers`, `claude-code-setup`.
- Faça login de novo em cada ferramenta (credenciais não estão aqui).
