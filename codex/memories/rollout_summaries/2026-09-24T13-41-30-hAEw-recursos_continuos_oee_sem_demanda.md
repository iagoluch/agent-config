thread_id: 01a0d3a6-5cd2-7422-8510-cc8de700d938
updated_at: 2026-09-28T17:42:32+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\09\24\rollout-2026-09-24T10-41-30-01a0d3a6-5cd2-7422-8510-cc8de700d938.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes
git_branch: master

# Recursos, calendário contínuo e OEE — implementação parcial, com validação automatizada

Rollout no repositório `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`. O usuário pediu que recursos inexistentes/removidos não apareçam, que recursos habilitados tenham presença contínua seguindo horários do sistema e que o cálculo de OEE fosse explicado sem pontas soltas para validação da Manufatura.

## Task 1: Remover recursos inexistentes da projeção

Outcome: success

Preference signals:

- O usuário disse: “esses recursos circulados não devem estar no sistema.” -> corrigir a fonte/projeção dos recursos, sem apenas ocultar superficialmente na tela.

Key steps:

- Identificada a causa: nomes brutos do catálogo eram projetados junto aos postos das contas ativas, criando cards-alias; não havia duplicação real de eventos ou apontamentos.
- Corrigidos os nomes canônicos em `app/core/resource_mapping.py`: `INSPE2` → `Inspeção Final`, `PREP` → `Preparação`, `ROBO P`/`ROBO S` → `Robô 1`.
- Códigos, eventos, apontamentos e histórico foram preservados; a sincronização futura não recria os nomes indevidos.

Reusable knowledge:

- A identidade do recurso deve ser resolvida pelo mapa canônico antes da projeção, sincronização ou criação de timelines; aliases não devem gerar recursos distintos.

References:

- Arquivo principal: `app/core/resource_mapping.py`.
- Testes: `tests/test_stage4c_resource_registry.py`, `tests/test_andon_redesign.py`.
- Validação reportada: 94 testes direcionados, `git diff --check` e reinício do backend TESTE com health OK/schema 49.

## Task 2: Presença contínua dos recursos e retorno de pausas

Outcome: partial

Preference signals:

- O usuário decidiu que todo recurso habilitado deve aparecer continuamente e que, ao terminar almoço/café, deve voltar ao estado anterior: “produção volta à mesma OP; parada continua na mesma parada/aguardando qualidade; sem demanda volta a sem demanda.” -> preservar snapshot completo, sem escolher estado por inferência nem criar OP.

Key steps:

- `ShiftBoundaryService` passou a obter recursos habilitados do catálogo (`listar_recursos_ativos_scheduler`), incluindo recursos sem histórico e futuros.
- Recursos sem calendário próprio herdam a janela global vigente, incluindo expediente e H1/H2 de `parametros_turno`; isso não cria capacidade/calendário individual artificial.
- Recursos com calendário próprio usam seus turnos e limites específicos.
- O fim de pausa restaura o evento físico anterior completo; se não houver snapshot, o fallback é Recurso sem demanda.
- O scheduler passou a inicializar recursos dentro do turno como `fila`/sem demanda, fora do turno como `fora_turno`, e respeita pausas configuradas.

Failures and how to do differently:

- A tentativa de reiniciar pelo inicializador falhou porque `iniciar_sistema_teste_cloudflare.py` não existe neste checkout; o processo existente na porta 8001 era Uvicorn direto. Não declarar a sincronização aplicada ao banco sem reiniciar pelo comando correto e conferir health/estado no TESTE.
- O agente auxiliar reportou 91 testes unitários, 4 testes PostgreSQL isolados, `py_compile` e `git diff --check` OK, mas também confirmou que o runtime não foi reiniciado; portanto a aplicação no banco TESTE permaneceu não verificada.

Reusable knowledge:

- Fonte canônica de recursos ativos: catálogo habilitado, agrupado por `resolve_resource_identity`; não usar lista estática, contas ativas ou somente recursos com eventos anteriores.
- `mes/services/calendar.py` deve usar o calendário específico quando existe e o fallback global quando não existe; análises de capacidade continuam `nao_configurado` sem vínculo próprio.

References:

- `mes/services/shift_boundary.py`.
- `app/database/database.py` (`listar_recursos_ativos_scheduler`, `finalizar_intervalo_automatico`, `interromper_recursos_ociosos_fim_turno`, `finalizar_fora_turno_automatico`).
- `mes/services/calendar.py` (`_default_operational_intervals`).
- Validações reportadas: 91 testes unitários dirigidos, 4 PostgreSQL isolados, `py_compile`, `git diff --check`; runtime não reiniciado.

## Task 3: Explicar e ajustar o cálculo de OEE

Outcome: partial

Preference signals:

- O usuário pediu: “me explique como o meu sistema faz o calculo de OEE, sem pontas soltas por favor, vou mandar à manufatura para conferência.” -> separar claramente fórmula, bases temporais, fontes de dados, casos sem dados e o que é regra atual versus ajuste implementado.

Key steps:

- A explicação entregue documentou o contrato backend: Disponibilidade = tempo trabalhado/tempo disponível; Performance = (tempo padrão das peças boas + setup/retrabalho/atividade sem OP)/tempo trabalhado; FTT = boas/(boas+refugo+retrabalho); OEE = Disponibilidade × Performance × FTT.
- OEE permanece calculado em `mes/analytics/oee.py`; frontend apenas apresenta valores.
- Produção, setup, retrabalho e atividade sem OP são produtivos; parada não planejada e desconhecido penalizam disponibilidade; parada planejada e fora de turno são retirados da base; fila vinculada a OP e fora de turno não entram.
- A mudança implementada passou a tratar `Recurso sem demanda` como tempo disponível sem produção: entra na base disponível e na base de performance, resultando em Disponibilidade 100% e Performance/OEE 0% quando ocupa sozinho o período. FTT permanece indisponível sem quantidade real.
- Testes foram atualizados para validar sem demanda separada em relatórios, sem derrubar disponibilidade e com OEE zero no período exclusivamente sem demanda.

Reusable knowledge:

- Não recalcular OEE no frontend nem mascarar ausência de dados como zero, exceto no caso explicitamente definido de período composto somente por sem demanda.
- Quantidade padrão usa `tempo_medio_segundos × quantidade boa`; refugo e retrabalho são separados, e retrabalho não completa a OP.
- O tempo físico é consolidado por recurso para evitar multiplicação de minutos quando há OPs simultâneas; rateio de OP é separado do tempo físico.

Failures and how to do differently:

- A implementação foi alterada e testada, mas a validação final no processo TESTE não foi concluída. Antes de divulgar como comportamento efetivo, reiniciar corretamente o Uvicorn em `127.0.0.1:8001`, consultar `/system/health` e verificar a projeção/OEE no banco `gestor_pecas_test`.

References:

- `mes/analytics/oee.py` (`calculate_oee`, `oee_seconds_by_category`, `OEE_CONTRACT`).
- `mes/services/management.py` (`standard_run_seconds`, timeline física, planned downtime e cálculo por recurso/setor).
- `mes/analytics/resource_state.py` (`physical_state_category`).
- Testes: `tests/test_oee_consistency.py`, `tests/test_no_demand_time_bucket.py`.
- Regra documentada para Manufatura: sem demanda = disponível sem produção; 100% disponibilidade, 0% performance/OEE quando isolado; FTT sem dado se não houver quantidade.
