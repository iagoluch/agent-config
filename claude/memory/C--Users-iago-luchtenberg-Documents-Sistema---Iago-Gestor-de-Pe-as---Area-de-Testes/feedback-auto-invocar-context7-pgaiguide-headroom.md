---
name: feedback-auto-invocar-context7-pgaiguide-headroom
description: "Invocar automaticamente context7, pg-aiguide e headroom quando relevante, sem esperar o usuário pedir — mesmo tratamento dado ao ponytail."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 75a23e2d-e8c2-44ad-b03f-c9289219fc68
  modified: 2026-09-22T12:17:53.749Z
---

Tratar `context7`, `pg-aiguide` e `headroom` como o `ponytail` ([[feedback-ponytail-toda-tarefa]]): usar proativamente quando o gatilho aparecer, sem o usuário precisar chamar cada vez.

**Why:** usuário pediu explicitamente (21/09/2026) o mesmo comportamento automático que já vale para o ponytail — não quer ficar re-pedindo essas ferramentas a cada tarefa.

**How to apply:**
- **context7**: sempre que eu for usar/explicar uma API de biblioteca ou framework (React, FastAPI, Vite, Vitest, etc.) e não tiver certeza absoluta do comportamento atual, consultar via `context7.sh` antes de responder ou escrever código, em vez de confiar em memória de treinamento potencialmente desatualizada.
- **pg-aiguide**: sempre que a tarefa envolver PostgreSQL de verdade (schema, query, migration, performance, indexação), consultar `mcp__plugin_pg_pg-aiguide__search_docs` (carregar via ToolSearch se ainda deferido) antes de propor a solução.
- **headroom**: REFORÇADO em 22/09/2026 — chamar `mcp__headroom__headroom_compress` em TODA mensagem/resposta desta sessão que envolva saída de ferramenta compressível (Bash, Grep, logs, JSON estruturado — não leitura de código via Read, que é excluída por design), sempre, sem julgar se "esta saída é grande o suficiente". Não é mais condicional a "se parecer volumosa" — é padrão incondicional. Ver [[headroom-uso-real-desktop]] para a limitação (proxy precisa estar de pé; sem ele o compress é no-op).

**Omniroute — REMOVIDO em 22/09/2026** (obsoleto, ver abaixo): usuário pediu para desativar por não usar mais. `claude mcp remove omniroute` executado; hook `SessionStart` (`omniroute-autostart.sh`) e o próprio script apagados do `.claude/settings.json`. Não reinstalar sem pedido explícito.

**Headroom — autostart do proxy, 22/09/2026**: para o item acima funcionar de verdade (não virar `router:noop`), criado hook `SessionStart` em `.claude/settings.json` chamando `.claude/hooks/headroom-autostart.sh` — mesmo padrão do antigo hook do omniroute: verifica `127.0.0.1:8787` via netstat (`LISTENING`), e se não estiver no ar, sobe `headroom proxy` a partir de `~/.headroom-run` em background. Best-effort, nunca bloqueia a sessão.

**Headroom — hook real de bloqueio, 22/09/2026**: além do autostart, criado `.claude/hooks/headroom-remind.sh` via `PostToolUse` (`Bash|Grep`) que bloqueia de verdade (`decision:block`) quando a saída passa de ~3000 bytes, pedindo `headroom_compress`. Ver detalhes e o hook irmão do ponytail em [[feedback-ponytail-toda-tarefa]]. Antes disso era só regra de memória; agora tem aplicação mecânica igual ao `graphify hook-guard`.
