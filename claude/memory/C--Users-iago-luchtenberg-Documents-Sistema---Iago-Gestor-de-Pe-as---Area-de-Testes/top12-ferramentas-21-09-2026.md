---
name: top12-ferramentas-21-09-2026
description: "Top 12 ferramentas/skills sugeridas em 21/09/2026 (pós-auditoria de 4 rodadas), com status real de adoção no sistema."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-21T17:44:21.122Z
  originSessionId: 75e7da9f-f422-46b4-9db7-52a8b071fa8b
---

Lista de 12 itens que o próprio Claude levantou em 21/09/2026 como candidatos de alto valor. Cruzada contra [[ferramentas-adotadas-auditoria-4rodadas]] e checagem rápida no código.

**Why:** usuário pediu para guardar a lista e saber o que já está implementado, sem reabrir decisão já tomada.

**Status:**
1. **eryxon-flow** (MES concorrente, catálogo de API) — NÃO aplicável a "implementar"; é referência externa para comparar cobertura de API, não uma ferramenta a instalar.
2. **pg-aiguide** — JÁ ADOTADO (plugin ativo, uso recomendado por padrão).
3. **Playwright CLI > MCP** — JÁ ADOTADO (`pytest-playwright`, `tests/test_e2e_smoke.py`, workflow `e2e.yml`).
4. **pybreaker + backon** — NÃO ADOTADO por decisão explícita; retry/backoff já resolvido em `mes/integrations/totvs/outbox.py`. Só reconsiderar com evidência real de flapping.
5. **totvs/engpro-advpl-tlpp-skills** — NÃO ADOTADO aqui; ADVPL/TLPP pertence ao repo separado `Protheus-AdvPL` (ver [[repo-protheus-advpl-separado]]).
6. **pg_partman** — NÃO ADOTADO; só se volume de tabela de eventos/apontamento degradar performance de forma mensurável.
7. **react-window** — NÃO ADOTADO (confirmado: sem `react-window` no `web/package.json`); só entra se uma tela nova tiver lista/tabela >500-1000 linhas sem paginação.
8. **gitleaks + bandit/Ruff-S + pip-audit** — JÁ ADOTADO e bloqueante de verdade no CI (sem `|| true`); bandit com 44 supressões `# nosec` já triadas.
9. **context7-skill** — JÁ ADOTADO (skill de baixo custo de contexto, usar em vez do MCP).
10. **i3x2ua (OPC UA)** — NÃO ADOTADO; não há integração OPC UA real no projeto hoje, é só atalho para um cenário futuro hipotético.
11. **schemathesis** — JÁ ADOTADO (`requirements-dev.txt`); já achou bug real (`GET /api/v1/audit/appointments` 500 em vez de 422 para ano 0263, ainda não corrigido — regra de negócio pendente).
12. **WCAG 2.3.2 (não piscar >3x/s)** — checado em `web/src/styles/global.css`: todas as animações são fade/slide/scale (fadeIn, scaleIn, slideInRight, fadeInUp, spin), nenhuma piscante. Andon/Solda não violam a regra hoje; não havia necessidade de correção.

**Resumo:** 5 já implementados (2, 3, 8, 9, 11), 1 sem violação a corrigir (12), 4 conscientemente não adotados por falta de gatilho (4, 5, 6, 7), 2 são apenas referências/ideias futuras sem ação (1, 10).
