thread_id: 01a09ff5-1ef0-7633-9968-54d037973fde
updated_at: 2026-09-10T18:43:07+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-16-01a09ff5-1ef0-7633-9968-54d037973fde.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 5.1 corrigiu as ressalvas da Simulação 2 e entregou quatro melhorias, com smoke dirigido sem erros

Rollout context: Projeto MES Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`. O usuário pediu explicitamente para não refazer a Wave 5 nem executar outra simulação completa; a ordem desejada era inspecionar, alterar, testar apenas o necessário, executar um smoke de aproximadamente 5 minutos e gerar relatório curto. O banco REAL deveria permanecer intocado e nenhum outbound produtivo deveria ser enviado.

## Task 1: Correções BUG-01, BUG-02, BUG-06 e BUG-07

Outcome: success

Preference signals:

- O usuário determinou: “Não refazer a Wave 5 do zero”, “Não fazer refatorações amplas sem necessidade” e “Não executar outra simulação completa de turno” -> em tarefas futuras, preservar o que já foi homologado e limitar a execução ao escopo corretivo solicitado.
- O usuário repetiu: “Não executar full suite repetidamente sem necessidade” e pediu testes direcionados durante o desenvolvimento -> priorizar testes por módulo/fluxo afetado; só executar uma suíte maior quando houver justificativa estrutural clara.

Key steps:

- A evidência da Simulação 2 foi reavaliada antes de alterar produto. O suposto BUG-01 não era defeito do backend: `SIM090001014/10` havia sido finalizada às 10:36 (seq. 277), antes da tentativa da `/20` às 10:57 (seq. 317). A correção foi feita no cenário do simulador (`scripts/simulacao_fabrica/plano.py`, campo `Trabalho.prioridade`) para realmente exercitar etapa anterior pendente; o portão de produção em `mes/services/operator_flow.py` foi mantido e testado.
- O estado de transição recebeu `explain_invalid_transition` em `mes/domain/operator_state_machine.py`, distinguindo ação já registrada, etapa finalizada, retomada incompatível e retorno incompatível, preservando `transicao_invalida` para compatibilidade.
- O rollup de Corte passou a usar `Database.listar_producao_corte_periodo` e os dados canônicos de `apontamentos_corte`/SigmaNEST, alimentando o setor, recurso e total gerencial somente quando os planos ativos da tarefa estão concluídos.
- `report_type` inválido passou a gerar `ReportError("report_type_invalido", status_code=400)` com handler em `backend/api/errors/__init__.py`; os cinco tipos válidos foram preservados.

Failures and how to do differently:

- O diagnóstico inicial do BUG-01 teria levado a uma alteração indevida no produto. Sempre verificar a ordem temporal dos eventos e o estado real antes de corrigir um bloqueio industrial.
- A execução inicial da Wave 5 falhou no fechamento por `TypeError` em `scripts/simular_fabrica.py:368`, causado por desempacotar `config.crachas` como tuplas embora fossem objetos `CrachaSimulacao`. O fix validado foi `[cracha.cracha for cracha in config.crachas]`.

Reusable knowledge:

- Wave 5.1 terminou com migration 27 somente em `gestor_pecas_test`; `gestor_pecas` REAL continuou no schema 11 e intocado.
- O smoke confirmou o override correto: 409, confirmação explícita, crachá autorizado e execução; concorrência também foi coberta.
- O rollup de Corte deve consultar a projeção canônica recém-criada, não fabricar números a partir do simulador.

References:

- Relatório: `docs/evidencias/simulacao_fabrica/wave5_1/RELATORIO_WAVE5_1.md`
- Evidência Simulação 2: `docs/evidencias/simulacao_fabrica/turno_20260914_wave5_sim2/eventos.csv`
- Arquivos principais: `mes/services/operator_flow.py`, `mes/domain/operator_state_machine.py`, `mes/services/management.py`, `app/database/database.py`, `mes/services/frontend_facade.py`, `backend/api/errors/__init__.py`

## Task 2: Ajustes do simulador

Outcome: success

Key steps:

- `tarefa_corte_incompleto` e `destaque_nao_liberado` passaram a ser classificados como `EXPECTED_BLOCK`.
- O agente de Laser passou a reler a fila após cada nesting, evitando estado obsoleto e duplicação de `corte_inicio`; a fila expõe `plano_hashes_em_processo`.
- O teste de recurso ocupado passou a usar outra OP e um posto livre, permitindo exercitar a causa pretendida.

Reusable knowledge:

- O simulador Wave 5.1 executou 89 passos, com 11 bloqueios esperados e zero erros no smoke.

## Task 3: Quatro pequenas melhorias funcionais

Outcome: success

Key steps:

- Setup: o backend calcula automaticamente `CONFORME`/`NÃO CONFORME` usando `referência ± margem`, limites inclusivos e precisão Decimal; o operador não escolhe mais manualmente o resultado.
- Tempo-pessoa: migration 27 e `mes/services/operator_participation.py` preservam múltiplos operadores por apontamento. O tempo da OP não é dividido; `tempo_pessoa_segundos` soma as participações, incluindo troca e concorrência.
- Apontamento incorreto: setor do roteiro e setor divergente são preservados, com histórico/auditoria sem reescrever eventos; a exibição pode identificar, por exemplo, `Dobra (Usinagem)`.
- Pintura: adicionadas as estações individuais Jato, Preparação, Pintura, Secagem e Inspeção Final, mapeadas para `JATO`, `PREP`, `PINT.L`, `ESTUFA` e `INSPE2`, mantendo um único login.

Validation:

- O agente reportou 328 testes unitários, 39 testes de integração PostgreSQL, 14 testes de UI, `tsc --noEmit` e 31 testes específicos de `tests/test_wave5_1.py` aprovados.
- O smoke cobriu os dez fluxos solicitados: primeira peça, retrabalho autorizado, retrabalho posterior, refugo, override, Corte no rollup, Setup, tempo-pessoa, apontamento incorreto e Pintura.
- `npm run build` em `web/` terminou com exit 0; houve apenas aviso de chunk maior que 500 kB.

Failures and how to do differently:

- Não houve validação visual/screenshots. A entrega deve ser considerada funcionalmente validada por payload/backend, não visualmente homologada.
- `RETOQ` e `TINTA` continuam sem posto por decisão de Manufatura; não criar logins ou seletores arbitrários sem nova decisão.

References:

- Testes: `tests/test_wave5_1.py`, `tests/test_quality_inspection.py`
- Código: `mes/domain/quality_measures.py`, `mes/services/operator_participation.py`, `app/core/operator_sectors.py`, `app/core/resource_mapping.py`, `mes/services/quality.py`

## Task 4: Smoke e relatório final

Outcome: success

Key steps:

- Smoke dirigido com seed `20260919`, 89 passos, duração aproximada de 20,4 segundos, 11 bloqueios esperados e 0 erros.
- Verificações de segurança confirmaram `gestor_pecas_test`, schema 27, `totvs_outbox` vazia, alertas internos 100% `PENDENTE` e nenhum outbound real.
- Relatório curto foi gerado e entregue em `docs/evidencias/simulacao_fabrica/wave5_1/RELATORIO_WAVE5_1.md`.

Reusable knowledge:

- Resultado final: Wave 5.1 aprovada, com ressalvas apenas para ausência de validação visual, mudança esperada na comparabilidade do OEE após incluir Corte no rollup e postos ainda não configurados para `RETOQ`/`TINTA`.
