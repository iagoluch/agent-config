---
name: ferramentas-adotadas-auditoria-4rodadas
description: "Ferramentas/skills/MCPs que a auditoria de 20/09/2026 (4 rodadas) deixou documentadas como ativas neste projeto — usar por padrão daqui pra frente, sem perguntar."
metadata: 
  node_type: memory
  type: project
  originSessionId: 75a23e2d-e8c2-44ad-b03f-c9289219fc68
  modified: 2026-09-22T12:03:53.309Z
---

Em 20/09/2026 o usuário pediu explicitamente para adotar, a partir de agora, tudo que ficou documentado como ATIVO/ADOTADO em `docs/CLAUDE_CODE_SETUP.md` e `docs/REFERENCIAS_TECNICAS.md`.

**Why:** auditoria de 4 rodadas já validou cada item na prática (testado de ponta a ponta, não só recomendado) — não é para reabrir a decisão a cada sessão.

**How to apply — usar sem pedir permissão:**
- **Skill `context7`** — consultar docs de biblioteca/framework via `context7.sh` em vez de confiar em memória desatualizada. `jq` já foi instalado em `~/.local/bin/jq.exe` (dependência da skill).
- **`graphify`** — já é regra fixa no `CLAUDE.md` do projeto: query/path/explain antes de grep cru para perguntas de arquitetura.
- **Playwright (`pytest-playwright`)** — E2E adotado de verdade, `tests/test_e2e_smoke.py`, workflow `e2e.yml` (`workflow_dispatch`, não bloqueia CI/deploy). Gotcha real: no Windows usar `./.venv/Scripts/python.exe`, não `python3` solto no PATH.
- **Schemathesis** — em `requirements-dev.txt`, já achou bug real (`GET /api/v1/audit/appointments` retorna 500 em vez de 422 para data extrema, ano 0263 — NÃO corrigido ainda, é regra de negócio pendente). Rodar contra `http://127.0.0.1:8010/api/openapi.json` quando for validar endpoints novos/alterados.
- **CI de segurança é bloqueante de verdade agora**: gitleaks + pip-audit + bandit, sem `|| true`. Bandit tem 44 supressões `# nosec BXXX -- motivo` já triadas individualmente — não adicionar nova supressão sem justificar com o mesmo padrão (motivo real, não "silenciar").
- **`headroom` (MCP)** — comprime bem output tipo Bash/grep/logs/JSON (28-94% de redução medida conforme conteúdo), mas NÃO comprime leitura de código-fonte via Read (exclusão por design). CORREÇÃO (22/09/2026): no app desktop, o proxy local (`headroom proxy`, porta 8787) NÃO fica rodando sozinho e as sessões do Desktop não conseguem rotear o tráfego real de API por ele (limitação confirmada por `headroom doctor`: "Desktop overwrites ANTHROPIC_BASE_URL", issue upstream #869). Sem o proxy ativo, `headroom_compress` é no-op (`router:noop`, 0 tokens salvos). Ver [[headroom-uso-real-desktop]] para o procedimento de uso manual que efetivamente funciona.
- **`pg-aiguide` (plugin)** — consultar para dúvidas de PostgreSQL/boas práticas. CORREÇÃO (21/09/2026): mesmo caso do headroom — disponível também no app desktop (`mcp__plugin_pg_pg-aiguide__search_docs`), não só no terminal.
- **`omniroute` (MCP)** — REMOVIDO em 22/09/2026 (`claude mcp remove omniroute`), a pedido explícito do usuário ("não estou usando"). Não é mais MCP registrado; hook `SessionStart` órfão (`omniroute-autostart.sh`) também removido do `.claude/settings.json` e o script apagado. Não reinstalar sem novo pedido explícito.

**O que NÃO adotar preventivamente (gatilho objetivo documentado, ainda não atingido):**
- `testcontainers-python` — REJEITADO, `TEST_DATABASE_URL` já cobre.
- `pybreaker`/`backon` — retry/backoff já resolvido em `mes/integrations/totvs/outbox.py`; só considerar circuit breaker se houver evidência real de flapping.
- `react-window` — só se uma tela nova tiver lista/tabela >500-1000 linhas sem paginação.
- `pg_partman` — só se volume de tabela de eventos/apontamento degradar performance de query de forma mensurável.
- `semgrep` — candidato a preencher lacuna de SAST em frontend JS/TS, mas não instalado ainda (evitar empilhar 2 SAST sem triagem).
- ADVPL/TLPP skills — pertencem ao repo `Protheus-AdvPL` separado, nunca a este.

Ver também [[gestor-pecas-github-cicd]] (CI/CD já validado) e [[repo-protheus-advpl-separado]] (por que ADVPL fica de fora).
