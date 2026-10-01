---
name: calendario-etapa4b-recursos-presos-fora-turno-25-09-2026
description: "25/09/2026 — recursos reais presos em Fora Turno no TEST: calendário de homologação ETAPA4B_TESTE_20260831 (só seg/ter) + c99f31b; desvinculado, backup no scratchpad"
metadata:
  node_type: memory
  type: project
  originSessionId: f46a0007-60dd-4c1f-8944-abddd50ee087
  modified: 2026-09-25T12:53:07.847Z
---

**Sintoma (25/09/2026, sexta):** na Consulta Operacional do TEST, os recursos realmente usados (LASER1, PLASMA, DOBRA1-3, JATO, PREP, PINT.L, INSPE2, CNC-02, TCNC-1, PREMTG, ROBO S) ficaram em "Fora Turno" desde 24/09 17:30, enquanto os ~300 recursos nunca usados voltaram às 08:00 ("Retorno do turno — recurso sem demanda").

**Causa:** 75 recursos do catálogo do TEST estavam vinculados ao calendário `ETAPA4B_TESTE_20260831`, que sobrou da homologação da Etapa 4B e só tem turnos em `dia_semana` 0 e 1 (seg/ter). O commit c99f31b (Codex, 24/09) fez o `ShiftBoundaryService.apply_due` tirar recursos com calendário próprio dos limites globais (`excluir_recursos=custom_codes`) e passar a usar só os eventos do calendário deles (`due_resource_calendar_events`). Na sexta esse calendário não tem nenhum turno, então nunca houve evento de "início" e eles ficaram presos. Antes do c99f31b isso não aparecia (o doc da Etapa 4B, §9, dizia que o calendário parcial "afeta apenas data_quality").

**Correção aplicada (só dados, só TEST):** `calendario_codigo = NULL` nos 75 recursos, e agora eles seguem `parametros_turno` como os outros. O ciclo seguinte liberou todos às 08:00 de forma retroativa. Backup do vínculo: `backup_vinculo_calendario_etapa4b.json` no scratchpad da sessão f46a0007. O REAL não tem nenhum vínculo de calendário e não foi afetado.

**Semântica mantida de propósito:** calendário próprio sem turno num dia significa recurso fora de turno nesse dia. Isso está certo para um calendário real (ex.: fim de semana de folga), então não mudei o código.

**Pegadinha de diagnóstico:** o servidor na 8001 usa `TEST_DATABASE_URL` (gestor_pecas_test), não `DATABASE_URL`. Consultar `DATABASE_URL` mostra outro banco, sem relação com a tela.

Ver também [[oee-reformulacao-24-09-2026]], [[regra-recursos-apontaveis-vs-sincronizados]].

**Continuação (mesmo dia) — usuário escolheu "apenas recursos em uso" na Consulta Operacional.** `consulta_operacional(somente_recursos_em_uso=True)` (frontend_facade) + `Database.listar_recursos_com_uso()` (apontamento operacional, apontamento de Corte ou evento físico manual). Mantém também postos de contas de operador ativas e qualquer recurso com execução agora. Ligado nos 3 endpoints de `/operations` (overview, resources, stream). TEST: 388 → 30. Andon, Capacidade e Dev Observatory não mudaram. Depois, a pedido do usuário, ROBO P e ROBO S viraram um card só: `_merge_shared_post_cards` (frontend_facade) + `shared_post_name` (resource_mapping). Resultado no TEST: 29 recursos.

**Correção do critério (mesmo dia):** o usuário pediu para seguir a regra que já tinha passado, [[regra-recursos-apontaveis-vs-sincronizados]], e não o histórico de uso. `somente_recursos_em_uso` passou a filtrar por `is_apontavel_resource` / `APONTAVEL_RESOURCE_IDENTITIES` (operator_sectors.py: postos de `OPERATOR_SECTORS` + código de estação). Execução em andamento continua sempre visível. `Database.listar_recursos_com_uso` foi removido. Também corrigido o posto "Secagem" da conta de Pintura, que aparecia como card extra ao lado do ESTUFA (`_post_identities` com `station_resource_code`). TEST: 34 cards, exatamente os postos da regra. O servidor 8001 agora roda pelo launch.json (`gestor-dev-observatory-8001`, Python 3.14 com --reload), então mudanças no código entram sem reiniciar.

**Timeline só de apontáveis (25/09/2026, tarde):** chave de dev `INCLUIR_RECURSOS_SO_SINCRONIZADOS = False` em app/core/operator_sectors.py (`participa_da_timeline`). Com ela desligada: o inventário do scheduler traz só os 26 apontáveis do catálogo mais 9 estações de solda sintéticas (Estação 1–6, Alumínio 1–3); `_transicionar_estado_recurso_tx` ignora escrita automática de não-apontável; `listar_estados_recurso_periodo`/`_atuais` escondem não-apontáveis, então sai das somas até o histórico antigo. Gotcha: o `sincronizado_em` da estação sintética = 1º estado dela ou agora (com None, o replay de 24h das pausas criou timeline retroativa; o artefato no TEST foi limpo). Pendência: Robô 1 = ROBO P + ROBO S, duas timelines, tempo em dobro na soma.

## Fechamento 25/09/2026 (tarde)
- **Destaque restaurado:** `APONTAVEL_RESOURCE_IDENTITIES` passou a incluir o nome de setor sem posto listado (Destaque e Montagem). Nenhum dado do Destaque foi apagado, ele só estava oculto pelo filtro.
- **Paradas automáticas** (intervalo almoço/café, `automatico=True`) ficam fora de `IndustrialAnalyticsService.downtimes`. Isso tira elas de: exceções, Maiores perdas, Recursos com maior impacto, análise de paradas, relatório de perdas, Telegram e IA. A composição física do tempo continua com elas, como parada planejada.
- **Robô 1 unificado:** `resolve_resource_identity` devolve "Robô 1" para ROBO P e ROBO S. No TEST:
  - ROBO S foi renomeado para "Robô 1" (17 estados, 1 apontamento, 1 quantidade);
  - foram removidas 12 duplicatas automáticas (ROBO P e Robô 1), com backup em `dev_reports/backup_robo_duplicatas_2026-09-25.json`;
  - o REAL não tem linhas de Robô.
- O servidor 8001 do usuário rodava **sem --reload** desde 13:31 (código velho gravando pausa em ALMOXS etc.). Foi reiniciado pela launch.json.
- As alterações de database.py desta tarefa entraram no commit 9abc7c2, feito pela sessão paralela.

**Padrão sem demanda (25/09/2026, a pedido):** recurso sem nada apontado é SEMPRE exibido com motivo "Recurso sem demanda", qualquer origem. Fonte única: `NO_DEMAND_REASON` em mes/domain/manufacturing_rules.py (usado por database.py, operator_flow, cut.py, frontend_facade). O retorno do turno mantém só o `tipo_interrupcao` "retorno_turno_sem_demanda" como marcador interno do Andon. 554 linhas antigas do TEST tiveram só o texto trocado; backups em dev_reports/backup_motivo_sem_demanda*_2026-09-25.json.

**Duplicação de recurso na Consulta Operacional (28/09/2026):** o estado físico grava a identidade canônica (`LASER1`, `DOBRA1`), enquanto Corte e apontamentos gravam o nome do posto (`Laser Ensis 3015`, `Gasparini`). A comparação pelo texto cru em `consulta_operacional` duplicava o Laser. A correção foi uma chave única, `_resource_key` (via `resolve_resource_identity`), em todos os cruzamentos de `mes/services/frontend_facade.py`. Qualquer cruzamento novo entre fontes deve usar essa chave, nunca `casefold()` do nome.

**28/09/2026 — Laser duplicado:** 33 linhas históricas de `eventos_estado_recurso` com recurso 'Laser Ensis 3015' migradas para LASER1 no TEST (backup em dev_reports/backup_laser_recurso_eventos_estado_2026-09-28.json). Migration 51 = CHECK NOT VALID `ck_eventos_estado_recurso_codigo_canonico` recusando nome de posto/alias como recurso (lista congelada `RESOURCE_STATE_FORBIDDEN_IDENTITIES`; `test_resource_state_canonical_constraint` exige migration nova quando o mapa de recursos ganhar nome). Depois (a pedido) os 5 legados que duplicavam também migraram: Gasparini→DOBRA1, 1303→DOBRA3, 2204→DOBRA2, Eurostec→CNC-02, Plasma TerraBlade 4→PLASMA (9 gêmeos idênticos removidos; backup dev_reports/backup_nomes_legados_eventos_estado_2026-09-28.json). Sobreposições resolvidas: apontamento/corte/intervalo é fato, preenchimento automático (sem demanda/fora turno) contido é removido e o que cobre evento real é recortado nas lacunas (13 removidas, 4 recortadas; backup dev_reports/backup_sobreposicoes_eventos_estado_2026-09-28.json). TEST: 0 nomes legados, 0 sobreposições. Porta 8000 (scripts/run_dashboard_api.py) não é usada — encerrada a pedido.
