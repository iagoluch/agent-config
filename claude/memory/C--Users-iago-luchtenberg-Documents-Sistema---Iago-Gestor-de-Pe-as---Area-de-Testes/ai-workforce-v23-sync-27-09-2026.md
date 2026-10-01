---
name: ai-workforce-v23-sync-27-09-2026
description: "IA Workforce V2.3 sincronizada e validada em 27/09/2026; drift QA corrigido, validator no CI, agentes não carregavam por YAML inválido (corrigido)."
metadata:
  node_type: memory
  type: project
  originSessionId: f89ad80a-9a52-4258-a783-a2569e50aa71
  modified: 2026-09-27T14:44:46.851Z
---

27/09/2026: master sincronizada com a workforce V2.3 (6 setores, 22 employees, 2 orchestrators, 4 specialists Impeccable sob frontend-engineer). Commits:
- `688ed7b`: QA tinha `technical-reviewer` como colaborador; passou a gate (`organization.json` + `ROUTING_MATRIX.md`). O validator entrou no job backend do CI.
- `8c5216d`: o CI **não rodava em push no master desde ef17e63 (20/09)**, porque `on.push` tinha só `tags-ignore`. Agora usa `branches: ["**"]`.
- `ebc0115`: os 22 agentes `.claude/agents/*.md` não carregavam, nem após restart. A `description` sem aspas continha `": "` → YAML inválido, descartado em silêncio. Aspas adicionadas e guard no validator. No mesmo commit, `GESTOR_EXPECTED_DATABASE` foi adicionado ao env do CI (a trava 506a92f derrubava 193 testes).
- `99cd75b`: `test_wave6d_solda_gerencial` estava desatualizado (f1a94a1 publica ROBO P como "Robô 1").
- `e531fc3` (28/09): specialists Impeccable via despacho do orquestrador a pedido do frontend-engineer (`SPECIALIST_REQUEST:`), porque subagente não abre subagente; technical-researcher com WebFetch/WebSearch; CLAUDE.md do projeto: delegar = workforce, não fast/standard/hard/extreme.
- `555d57c` (28/09): **workforce global**. `scripts/install_global_workforce.py` copia os 26 agentes para `~/.claude/agents/` (caminhos absolutos para `.ai/`, marcador no topo) e liga as 8 skills via junction; roda no SessionStart do projeto. Agentes genéricos fast/standard/hard/extreme **eliminados** (backup em `~/.claude/agents-backup-2026-09-28/`, junto com `CLAUDE.md.bak`); o roteador do `~/.claude/CLAUDE.md` global virou R0–R3 da workforce.

**Why:** o CI desligado escondeu o drift e as regressões por 1 semana.
**How to apply:** cópia global nunca se edita à mão (é sobrescrita); agente da workforce "not found" → rodar `python scripts/validate_ai_workforce.py` antes de suspeitar de restart. Agentes só aparecem após reiniciar a sessão. Ver [[gestor-pecas-github-cicd]].
