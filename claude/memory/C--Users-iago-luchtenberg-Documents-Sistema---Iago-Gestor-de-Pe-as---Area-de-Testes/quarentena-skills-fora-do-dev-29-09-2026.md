---
name: quarentena-skills-fora-do-dev-29-09-2026
description: 19 skills sem relação com desenvolvimento movidas (não apagadas) do Claude e do Goose para ~/.claude/skills-quarentena-2026-09-29/ com aprovação do usuário.
metadata:
  type: project
---

Em 29/09/2026, com "sim" explícito do usuário, 19 skills fora do escopo de desenvolvimento saíram de `~/.claude/skills` (58 restantes) e de `~/.agents/skills` (cópias do Goose, instaladas em 14/09):
competitive-ads-extractor, domain-name-brainstormer, invoice-organizer, lead-research-assistant, raffle-winner-picker, tailored-resume-generator, twitter-algorithm-optimizer, video-downloader, slack-gif-creator, skill-share, template-skill, meeting-insights-analyzer, brand-guidelines, langsmith-fetch, file-organizer, image-enhancer, content-research-writer, internal-comms, canvas-design.

Destino: `~/.claude/skills-quarentena-2026-09-29/` (Claude) e `.../_agents-goose/` (Goose). Nenhuma estava em `composio-skills`, então `configure-skills.bat` não as recria. Sync do Goose depois: 0 conflitos, 0 drift.

**Why:** 0 uso em setembro; cada descrição de skill entra em toda sessão e compete na escolha automática.
**How to apply:** para restaurar, mover a pasta de volta para `~/.claude/skills/` (e `_agents-goose/<nome>` para `~/.agents/skills/`). Não reinstalar sem pedido explícito. Relacionado: [[limpeza-skills-composio-automation]], [[feedback-delegacao-e-council-autorizados]].
