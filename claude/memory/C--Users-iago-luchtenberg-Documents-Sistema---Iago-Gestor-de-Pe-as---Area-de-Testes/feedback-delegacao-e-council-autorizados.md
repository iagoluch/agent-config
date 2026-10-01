---
name: feedback-delegacao-e-council-autorizados
description: "29/09/2026: usuário autorizou permanentemente delegar à workforce e rodar llm-council; exige linha 'Roteamento:' no fim de cada resposta de tarefa."
metadata:
  type: feedback
---

O usuário notou que o llm-council e os 26 funcionários da workforce não eram usados. Os logs de set/2026 confirmaram: council 0 usos, funcionários 2 chamadas desde 28/09, skills de fluxo 0 usos. Só `ponytail` e `task-observer`, que têm hook, eram usadas.

Correção aplicada:
- autorização permanente no CLAUDE.md global (protocolo de roteamento);
- hook global `UserPromptSubmit` `~/.claude/hooks/workforce-routing-reminder.sh`;
- linha de visibilidade `Roteamento: R<n> · <agentes|direto|Nemotron> · skills <…>`.

**Why:** a instrução do ambiente ("não abrir subagente sem pedido"), somada a "R0 direto", "Delegation efficiency", [[feedback-nao-fragmentar-em-agentes-em-massa]] e "não anuncie a classificação", fazia fazer tudo sozinho parecer o caminho seguro. Uma skill que depende só da descrição não dispara.

**How to apply:**
- R1+ vai para 1 owner da matriz, mais a skill de fluxo;
- decisão com tradeoff real vai para o `llm-council`, nunca em sim/não;
- fechar a resposta com a linha `Roteamento:`;
- se a linha começar a faltar ou o council ficar sem uso de novo, conferir se o hook ainda está registrado em `~/.claude/settings.json`.

**Skills do projeto (29/09/2026, 11:25):** medição de set/2026 — 77 skills instaladas, 15 usadas (quase só task-observer/ponytail, que têm hook). As 8 skills do repo (`.claude/skills/`: industrial-change, integration-change, architecture-review, security-review, current-docs, change-verification, release-gate, ai-orchestrate) tinham 0 uso porque só os funcionários as citavam; a sessão principal não tinha mapeamento. Corrigido: seção "Skills do projeto" no CLAUDE.md do projeto + hook de roteamento dizendo que skill do projeto prevalece sobre a tabela genérica. Medir de novo em ~1 semana para confirmar que disparam.
