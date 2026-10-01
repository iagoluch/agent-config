---
name: opencode-memoria-inbox
description: "Memória do OpenCode/Nemotron: lê o MEMORY.md do Claude e grava só em memory/inbox/; o Claude revisa no SessionStart"
metadata:
  node_type: memory
  type: project
  originSessionId: 4cb95d48-78e1-430a-97fe-d1215ceeda90
  modified: 2026-09-28T13:05:52.039Z
---

Desde 28/09/2026 o Nemotron (OpenCode) compartilha a memória deste projeto:
- Lê o `MEMORY.md` via plugin global `.opencode/global-plugins/claude-compat.js` (copiado para `~/.config/opencode/plugins/` por `scripts/export_opencode.py`).
- Grava memórias novas com a ferramenta `memoria_salvar` **apenas** em `memory/inbox/` (frontmatter com `source: opencode-nemotron` e `created`).
- O hook `~/.claude/hooks/memory-inbox-check.py` (2º hook do SessionStart em `~/.claude/settings.json`) avisa o Claude quando há arquivos em `inbox/*.md`.

- Os plugins (`claude-compat.js` global e `.opencode/plugins/claude-hooks.js`) têm formato duplo: o `export default` traz `id`+`setup` (OpenCode 2.x, o Desktop do usuário) e `server` (CLI 1.18.x no PATH). Sem `setup`, a 2.x recusa o plugin em silêncio. Foi a causa real da falha do teste de fumaça de 28/09 (memória, graphify e type-check ausentes).
- Na 2.x as ferramentas MCP (ex.: headroom) ficam dentro de `execute` (code mode). "Indisponível" costuma ser nome errado, não MCP fora do ar.

**Why:** o usuário escolheu a opção "caixa de entrada revisada pelo Claude" (e não escrita direta), para o Nemotron não poluir nem contradizer a memória canônica.

**How to apply:** quando o hook listar memórias pendentes, promova (mover para memory/, tirar source/created, mesclar duplicadas e indexar no MEMORY.md) ou descarte movendo para `inbox/_descartadas/`, nunca apagando. Relacionado: [[ai-workforce-v23-sync-27-09-2026]].
