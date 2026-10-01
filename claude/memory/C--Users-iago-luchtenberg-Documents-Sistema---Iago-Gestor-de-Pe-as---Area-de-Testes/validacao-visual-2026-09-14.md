---
name: validacao-visual-2026-09-14
description: "Validação visual completa rodada em 2026-09-14 — 55 telas cobertas, 8 defeitos corrigidos, densidade do Andon TV documentada sem alterar, 1 decisão de breakpoint pendente"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-14T06:22:00.492Z
---

Relatório completo: `docs/VALIDACAO_VISUAL_2026-09-14.md`. 55 telas/estados cobertos (≥2 larguras cada; Andon/Solda também em 1920×1080; login do Dev Observatory também em 420px), com um auditor de layout injetado (mede `getBoundingClientRect()`+estilo computado, detecta texto cortado, overflow, alturas desiguais na mesma linha de grid, sobreposição real, fonte <10px).

**8 defeitos corrigidos:**
- Fonte inconsistente nos cartões de KPI (23px vs 17px pra mesma frase).
- 4 casos de texto cortado (detalhe do KPI, Pareto de Paradas, ranking de Atrasos da Solda, rótulos do gráfico de MACRO).
- Solda quebrada a 1024px + login do Dev Observatory sem meta viewport (renderizava a 980px lógicos no celular).
- Nome do operador com reticências na sidebar inconsistente com o bloco gerencial vizinho.
- **Achado que não era CSS**: `MetricCard` recebia `availability={x?.availability}` e caía no default `"disponivel"` quando o indicador inteiro vinha ausente do backend — cartão parecia ter número quando não tinha. Corrigido com `metricState()` em `AnalyticsPages.tsx`.

**7 achados documentados sem alterar** — principal: densidade do Andon TV (18 textos <10px, 8 cortados a 1920×1080), consequência direta da decisão "tudo cabe sem rolagem" — corrigir é redesenhar a tela, não CSS. Também: `.andon-header` é CSS morto (AndonPage não renderiza mais cabeçalho), "Management View" em inglês (consistente, afirmado em testes), 3 achados de dado do fixture da preview (não do produto real).

**Decisão pendente (baixo risco, fácil reverter):** o agente moveu o breakpoint de `.welding-macros__body` de 900px para 1180px (mesmo valor que `global.css` já usa em outros lugares) porque a 1024px a tabela pivô da Solda comia a largura e sobravam só 280px pro gráfico de 7 MACROs. Se 1024px não for uma largura de uso real no chão de fábrica, é seguro reverter — é uma linha só.

**Validação:** `tsc -b` limpo; suíte frontend completa 156 testes passando (rodou a suíte inteira por ter tocado `global.css`); `test_dev_observatory` 19/19; auditor com 0 achados nas 34 rotas gerenciais, Solda (TV+gerencial), Operador; TV do Andon/Solda seguem sem rolagem.

**Arquivos alterados:** `web/src/pages/analytics/AnalyticsPages.tsx`, `web/src/styles/global.css`, `web/src/styles/welding.css`, `backend/api/routers/dev_observatory.py` (só CSS/HTML das páginas de login/recusa).

**Why:** pedido explícito do usuário em 2026-09-14 ("design perfeito... sem card na frente do outro"). Terceira auditoria do dia, depois de [[auditoria-seguranca-2026-09-14]] e [[pente-fino-2026-09-14]] — todas as 3 rodaram/terminaram no mesmo dia.

**How to apply:** se quiser reverter o breakpoint de 1024px, é em `web/src/styles/welding.css` na regra `@media (max-width: 1180px)` do `.welding-macros__body` — trocar de volta pro valor antigo (900px) é a única mudança necessária.
