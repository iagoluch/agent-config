---
name: wave5-estado
description: Estado das Waves 5 e 5.1 (primeira peça + crachá + PDF + Setup automático + tempo-pessoa + apontamento incorreto + estações de Pintura).
metadata: 
  node_type: memory
  type: project
  originSessionId: 11ada5d5-946c-4d91-afdd-12d961d4de56
  modified: 2026-09-10T18:42:44.770Z
---

## Wave 5 (2026-09-10) — APROVADO COM RESSALVAS
Nova lógica industrial: gate da "primeira peça" (produz 1ª peça → Setup quando a operação tem → inspeção pelo próprio operador → CONFORME → libera o lote; Finalizar bloqueado no back e no front até isso); retrabalho da 1ª peça → OP BLOQUEADA → liberação só por crachá autorizado (SIM99 ok / SIM00 não), exclusivo p/ retrabalho da 1ª peça, refugo NÃO exige crachá; alertas internos preparados p/ Telegram (`canal_previsto=telegram`, `status_notificacao=PENDENTE`, nada enviado); visualizador de PDF (backend resolve por LastWriteTime, modal escurecido).

Arquivos base: `mes/domain|services/first_piece.py`, `app/database/first_piece_repository.py`, `mes/domain|services/internal_alerts.py`, `mes/services/drawings.py`, `web/src/pages/operator/WorkbenchPage.tsx`, `web/src/pages/home/BadgesPage.tsx`. Migration 26 = WAVE5_FIRST_PIECE.

Simulação 2: `docs/evidencias/simulacao_fabrica/turno_20260914_wave5_sim2/` (RELATORIO_SIMULACAO_FABRICA.md + JSONs). Carga 17–19 recursos no pico. KPIs backend: Disp 85,95 / Perf 38,56 / FTT 99,43 / OEE 32,95; `standard_run_seconds=134803`. 0 erros técnicos, 22 agentes.

## Wave 5.1 (2026-09-14) — aprovado
`docs/evidencias/simulacao_fabrica/wave5_1/RELATORIO_WAVE5_1.md`.
- **BUG-01 não era bug de produto** — a evidência da Sim 2 estava mal diagnosticada (a etapa anterior JÁ tinha sido finalizada). O portão `operator_flow._etapa_anterior_pendente` está certo; corrigido o cenário do simulador (`plano.py` novo `Trabalho.prioridade`). Gate coberto por teste normal+concorrente.
- **BUG-02** — `mes/domain/operator_state_machine.py::explain_invalid_transition` (acao_ja_registrada / etapa_ja_finalizada / retomada_incompativel / retorno_incompativel); `details.codigo_generico="transicao_invalida"` preservado p/ compat.
- **BUG-06** — Corte estava fora do rollup gerencial porque vive em `apontamentos_corte`. Nova projeção `Database.listar_producao_corte_periodo` (soma `catalogo_sigmanest_ops.quantidade` quando todos os planos ativos da tarefa finalizaram), consumida em `mes/services/management.py`. **Consequência: produção do Corte agora entra em quantidade global e FTT/OEE — OEE não é mais comparável direto com a Sim 2.**
- **BUG-07** — `frontend_facade` levanta `ReportError("report_type_invalido",400)`; handler em `backend/api/errors/__init__.py`. Tipos válidos: gerencial|producao|perdas|indicadores|dados_analiticos.
- **Melhoria 1 — Setup conformidade automática**: `mes/domain/quality_measures.py` (Decimal, limite fechado, mm). Backend calcula CONFORME/NAO_CONFORME; operador só digita a medida. Status do cliente só vale p/ template legado texto livre. UI: `QualityInspectionPage.tsx` (indicador no lugar do select).
- **Melhoria 2 — tempo-pessoa**: `participacoes_operador` ganhou `apontamento_id/tipo_participacao/operador_principal` + índice único parcial `uq_participacao_aberta_apontamento` (migration 27). `mes/services/operator_participation.py` chamado por `operator_flow.executar`. Tempo da OP NÃO é dividido; `traceability.person_time` publica `tempo_pessoa_segundos` = soma das participações.
- **Melhoria 3 — apontamento em setor incorreto**: migration 27 adiciona `setor_roteiro`+`setor_divergente` em `apontamentos_operacionais` e `eventos_apontamento_operador` (gravado 1x via COALESCE, histórico nunca reescrito). `app/core/operator_sectors.sector_display_label` → `Atual (Original)` ex.: `Dobra (Usinagem)`.
- **Melhoria 4 — estações de Pintura**: `PAINTING_STATIONS = (Jato, Preparação, Pintura, Secagem, Inspeção Final)` em `app/core/operator_sectors.py`, **um único login `operador_pintura`**, sem seletor. PC Factory já tem máquina por etapa (`JATO/PREP/PINT.L/ESTUFA/INSPE2`) → cada estação pareada com o código exato em `app/core/resource_mapping.py` (diferente de Solda que compartilha). `RETOQ`/`TINTA` seguem sem posto (decisão de Manufatura).

**Migration 27** = tempo-pessoa por apontamento + rastreabilidade de setor incorreto. **SÓ em `gestor_pecas_test` (schema 27). REAL `gestor_pecas` = schema 11, intocado.**

Testes: 328 unitários + 39 integração PG + 14 UI + `tsc --noEmit` OK. `tests/test_wave5_1.py` (31 testes). 1 teste homologado reescrito (o que exigia o operador escolher CONFORME — substituído pela Melhoria 1; teste irmão preserva a regra p/ template legado). Smoke `scripts/smoke_wave5_1.py` seed 20260919, 89 passos, 11 EXPECTED_BLOCK, 0 erros, 20s.

`npm run build` do `web/` feito (2026-09-14, exit 0). Sem validação visual (screenshots).

Ver [[wave4-estado-fechamento]] e [[feedback-economia-de-tokens]].
