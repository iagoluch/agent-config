---
name: oee-reformulacao-24-09-2026
description: Reformulação do OEE conforme PROMPT_OEE rev.01 — o que foi implementado (commit ad8410a) e o que depende de Gabriel Fogaça
metadata:
  node_type: memory
  type: project
  originSessionId: 2f57d858-29a6-41d3-9ebe-7d1f80863f0e
  modified: 2026-09-25T16:36:28.060Z
---

Prompt que governa: `Downloads/PROMPT_OEE_Gestor_de_Pecas_MES.md` (rev. 01, 24/09/2026). Responsável funcional: Gabriel Fogaça.

Implementado e commitado em 24/09/2026 (ad8410a, auto-push autorizado pelo usuário):
- `mes/analytics/oee.py`: sem demanda fora das duas bases (C08); exceção explícita 100/0/0 com origem `REGRA_CORPORATIVA_SEM_DEMANDA` e FTT NOT_APPLICABLE; removido o atalho genérico `P==0 → OEE=0`; tempo padrão ausente bloqueia a Performance (NOT_CONFIGURED) ou a marca como PARCIAL; Performance >100% mantém o valor bruto e o alerta; metodologia/versão (`corporativa-2026-09-24`) em `OEE_CONTRACT` e `trace_dict()`.
- `mes/services/management.py`: `good_without_standard` (linhas sem `tempo_medio_segundos` + boas do Corte vindas de nesting); `kpi_calculation` no global e por recurso, com a consolidação marcada `PENDENTE_HOMOLOGACAO`.
- Testes: `tests/test_oee_corporate_rules.py` (novo) + 2 testes ajustados que codificavam a regra do Codex (sem demanda dentro das bases).

**Why:** o commit c99f31b (Codex) tinha colocado sem demanda nas duas bases, o que violava C08; e no REAL o TOTVS grava NULL em tempo_medio_segundos, então a Performance aparecia perto de 0 como se fosse um valor real.
**How to apply:** no REAL, Performance/OEE vão aparecer "não configurado" até existir tempo padrão; isso é esperado, não é bug. Pendências da seção 14 continuam com o Gabriel (consolidação da exceção, base do período misto, tempo padrão, Corte).

Etapa seguinte (24/09/2026, commit b5a66de, pushed): estado físico do recurso em `app/database/database.py`.
- Fim da última OP/nesting → `_entrar_sem_demanda_tx` abre `fila` sem OP (`recurso_sem_demanda`), sem lacuna; preserva intervalo automático e `fora_turno` abertos.
- Fim do intervalo automático restaura o snapshot, mas se ele veio de OP/nesting (`EXECUTION_STATE_ORIGINS`) que terminou na pausa → sem demanda (I03).
- Pegadinha: apontamento guarda o código do posto (`1303`), estado guarda a identidade canônica (`DOBRA3`) — comparar sempre via `resolve_resource_identity`.
- Testes: `tests/test_resource_state_no_demand_and_break.py` (PostgreSQL real, 7 cenários). `test_pausa_automatica_inclui_recurso_habilitado_nunca_usado` falha também ANTES da mudança (depende da hora do dia) — pré-existente.
- Decisão do usuário: execução encerrada fora da janela operacional (após expediente + hora extra planejada, via `CalendarService.shift_window_kind`) → `fora_turno`/`fim_turno`; dentro da hora extra planejada → sem demanda.
- Regra do intervalo REVISADA pelo usuário (24/09, vale também p/ Corte; checado que não afeta OEE — produção na pausa conta como trabalhado, conforme PROMPT_OEE §6): apontar produção/setup/retrabalho na pausa sobe o recurso (`inicia_trabalho` no reconcile); encerrada ainda na janela configurada → volta para a pausa (`_entrar_sem_demanda_tx` → `_abrir_intervalo_tx` via `ShiftBoundaryService.active_break`); aberta até o fim → segue como está (o fim só mexe em linha de pausa aberta). Parada apontada na pausa mantém a pausa (não vira parada não planejada). Registrar quantidade não é transição de estado.
- H1/expediente/H2 já é genérico (vem de `parametros_turno`, recarregado a cada ciclo): limites = fim do expediente + fim de cada hora extra; OP finalizada em H1/H2 → sem demanda; limite → fora_turno; início do expediente só converte fora_turno. Seed: H1 06:00-08:00, H2 17:30-21:30.
- Validação pedida pelo GPT do Gabriel (25/09/2026, commitada junto com OP programada/vigência): cenários A–F com bases do OEE em `tests/test_resource_state_no_demand_and_break.py` (helper `_oee_bases`). Única mudança de produção: `iniciar_intervalo_automatico` pula máquina com nesting 'Em processo' (decisão do usuário: Corte "segue em produção" no almoço). Teste `..._nunca_usado` corrigido com `patch.object(db, "_now")` (sincronizado_em do relógio real > instante fixo da pausa).
- **REMOVIDA em 28/09/2026 a pedido do usuário** ("esse aviso global de op programada eu não quero"): `_fila_sem_execucao_tx` e `SCHEDULED_OP_*` apagados; fila sem execução é SEMPRE "Recurso sem demanda" em todos os setores. Não reintroduzir sem pedido explícito. Dados do TEST limpos no mesmo dia (13 linhas de eventos_estado_recurso → sem demanda, backup dev_reports/backup_op_programada_eventos_estado_2026-09-28.json). O servidor :8000 (scripts/run_dashboard_api.py, iniciado 27/09, sem reload) precisa reiniciar para parar de gravar o aviso. Histórico: OP programada (definição do usuário 25/09: "OP dentro do TOTVS aguardando ser apontada") = operação ativa em catalogo_operacoes_op + OP ativa em catalogo_pcp_ops, recurso resolvido = este, sem apontamento não-'Aguardando' (op+numero_operacao). `Database._fila_sem_execucao_tx` decide: fila com OP (tipo `op_programada`, QUEUE) ou sem demanda. Usado no fim da última OP, fim do intervalo (sem demanda não é restaurado às cegas) e retorno do turno. 'Aguardando' continua NÃO contando (resíduo de início recusado). No TEST quase todo recurso tem OP pendente (~1915 OPs ativas) → sem demanda ficou raro; risco de OPs mortas no catálogo segurarem fila (levado ao Gabriel).
- `parametros_turno` TEM vigência (migration 50, `parametros_turno_historico` [vigente_desde, vigente_ate)); `load_manufacturing_rules(db, vigente_em=...)`; só `_fora_do_turno` usa por enquanto (audit.py/ShiftBoundaryService ainda usam o atual).
- Pontos abertos (Corte P via SigmaNEST tempo_previsto_segundos, FTT, tempo padrão SG2 G2_TEMPAD, consolidação, versão da regra) com propostas em `docs/OEE_PONTOS_ABERTOS_PROPOSTAS_2026-09-25.md` — aguardando Gabriel.
- Testes usam t0 fixo (22/09/2026 09:00) — não depender da hora do dia. Pegadinha: o evento `fila` do enfileiramento usa o relógio real, então com t0 no passado a interrupção de fim de turno vê "evento posterior" e só corrige retroativamente — o helper `_started_op` realinha esse evento. `apontamentos_corte` tem ON CONFLICT (plano_hash): um nesting só inicia uma vez.
