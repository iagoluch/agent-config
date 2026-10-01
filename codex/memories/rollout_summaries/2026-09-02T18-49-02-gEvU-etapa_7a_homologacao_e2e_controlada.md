thread_id: 01a06374-0157-7e81-987b-81a40bafa8aa
updated_at: 2026-09-02T20:29:20+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\09\02\rollout-2026-09-02T15-49-02-01a06374-0157-7e81-987b-81a40bafa8aa.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Etapa 7A foi implementada e validada localmente, mas permaneceu parcial por não executar novos movimentos no WSPCP TESTE real

Rollout context: projeto Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, PowerShell, banco TESTE `gestor_pecas_test`. O usuário exigiu reutilizar a arquitetura canônica, substituir somente a fronteira `GPOPSYNC → ProductionOrder`, não alterar `GPOPSYNC.prw`, não investigar novamente APIs TOTVS padrão e separar claramente confirmado, não executado e bloqueado.

## Task 1: Homologação E2E controlada da Etapa 7A

Outcome: partial

Preference signals:

- O usuário determinou que o único componente controlado deveria ser `HTTP GPOPSYNC → XML ProductionOrder`, sem segundo parser, mapper, máquina de estados, tabela de OP ou fluxo de apontamento -> em tarefas equivalentes, preservar a fronteira e reutilizar integralmente os serviços canônicos.
- O usuário pediu explicitamente que a OP ausente percorresse o fluxo normal e que o relatório distinguisse “CONFIRMADO”, “NÃO EXECUTADO” e “BLOQUEADO” -> futuras homologações devem evitar declarar sucesso externo quando apenas fixtures ou ACKs controlados foram usados.
- O usuário não autorizou novo envio empresarial sem OP descartável confirmada; o agente manteve o WSPCP de negócio real desligado e exigiu confirmações literais para `--send`.

Key steps:

- Antes de editar, foram lidos `AGENTS.md`, `ROADMAP.md`, `README.md`, documentação TOTVS e implementações de inbound, outbox e OP sob demanda.
- Confirmado que o checkout não tinha metadados Git utilizáveis; alterações foram acompanhadas diretamente por arquivos.
- Criado `scripts/homologar_totvs_e2e_etapa7a.py`, um orquestrador reproduzível que cria schema efêmero em `gestor_pecas_test`, inicia responder HTTP local no contrato `GESTORPECASPO`, devolve sem reconstrução a fixture real `tests/fixtures/totvs/ok_productionorder_20260821103018_1079689c001 1.xml` e remove o schema ao final.
- Criado `tests/test_totvs_etapa7a_e2e.py`, usando HTTP real para provisionamento e ACK controlado somente na fronteira do worker.
- Reutilizada a OP `1079689C001`, fixture SHA-256 `948849e2f146cba100b4a52da3601b88b519d85541475e17d8c529d3cd5b1ae3`, `SourceApplication=SIGAPCP`, produto `MATA650 12.1.2510`.
- Provado: lookup inicial MISS; duas requisições concorrentes geraram exatamente uma chamada HTTP; o pipeline canônico ingeriu a OP; uma segunda consulta foi local; o inbox recebeu uma mensagem; nenhuma outbox foi gerada pela ingestão.
- Provado o roteiro recebido na ordem original e a projeção segura: `10/CORTE/LASER` virou recurso canônico `LASER1`; `99/FINALIZADA/ALMOX4` foi preservado uma vez como `marco_terminal=true`, `ativo=false`, sem setor e invisível ao operador.
- A auditoria read-only `scripts/auditar_sigmanest.py --wo 1079689C001` não encontrou correlação SigmaNEST; o cenário foi registrado como não aplicável, sem fabricar nesting ou OP.
- Executado pelo `OperatorFlowService`: `Início → Parada → Retomar → Finalizado parcial → Finalizado`, sem inserir fatos produtivos via SQL. Resultado: 1 apontamento, 6 eventos do operador, 3 eventos de recurso, 7 históricos, 2 peças boas, 1 refugo e 0 retrabalho.
- Geradas quatro obrigações outbound atômicas: `StopReport`, apontamento parcial, finalização e marco terminal. O terminal usou 2 boas reais, não contou refugo e não completou pela quantidade planejada.
- Provados `PENDING → SENDING → RETRY`, preservação das quatro chaves/payloads, restart, recuperação de item `SENDING` por lease e recusa de tentativa duplicada do terminal.
- O teste automatizado levou os quatro itens a `SENT` com ACK controlado; isso valida o worker/outbox, não o negócio no Protheus.
- Atualizados `ROADMAP.md`, `README.md`, `protheus/README.md`, `docs/INTEGRACAO_TOTVS_OP_SOB_DEMANDA_ETAPA61.md` e criada `docs/evidencias/TOTVS_ETAPA7A_HOMOLOGACAO_CONTROLADA_2026-09-02.md`.
- Verificado ao final: banco efetivo `gestor_pecas_test`, zero schemas `etapa7a_*` remanescentes e zero itens adicionais em `public.totvs_outbox`.

Failures and how to do differently:

- A primeira execução do novo script consultou a tabela inexistente `catalogo_sigmanest_pecas`; o nome correto no schema é `catalogo_sigmanest_ops`. Ao criar novos instrumentos, conferir os nomes efetivos em `app/database/migrations.py` antes de executar.
- Uma consulta SQL com `LIKE 'evento_apontamento:%'` foi passada incorretamente como placeholder do psycopg; corrigiu-se para `LIKE %s` com parâmetro separado. Sempre parametrizar o padrão SQL, sem inserir `%` diretamente no texto usado pelo driver.
- O primeiro fluxo gerou `StopReport` sem payload porque o relógio dos eventos não era monotonicamente avançado. A solução foi injetar `_AdvancingClock` no `OperatorFlowService`; homologações sintéticas devem controlar o tempo para garantir ordem causal.
- A suíte completa exibiu logs de falhas deliberadamente injetadas por testes de atomicidade e provedores indisponíveis; o resultado final foi `Ran 574 tests ... OK (skipped=1)`, portanto esses logs não representaram regressões.
- O WSPCP TESTE real não foi chamado nesta rodada. A Etapa 7A não deve ser considerada homologação empresarial completa até existir uma OP autorizada e haver ACK/efeito externo verificável.

Reusable knowledge:

- O responder controlado da 7A usa a rota `/rest/GESTORPECASPO/gestorpecas/v1/production-order` e devolve byte a byte uma mensagem `ProductionOrder` real; ele não reconstrói XML nem contém regra de negócio.
- A fronteira canônica validada é `OrderProvisioningService → ProductionOrderOnDemandSyncService → ProtheusOnDemandRequestGateway → TotvsProductionOrderIngestionService → catálogo → OperatorFlowService → fatos canônicos + outbox → TotvsOutboxWorker`.
- O terminal `99/FINALIZADA/ALMOX4` deve existir no catálogo, permanecer inativo e invisível ao operador; sua emissão só ocorre após todas as operações apontáveis concluídas.
- Retry, restart, lease e reprocessamento devem reutilizar a mesma `idempotency_key` e o mesmo payload; transporte é at-least-once, não exactly-once.
- SigmaNEST é somente leitura e não pode criar OP. Para `1079689C001`, a ausência de correlação foi comprovada e registrada como “não aplicável”.
- O endpoint Protheus `GESTORPECASPO` está publicado e alcança o ADVPL, mas a chamada com `ZZ00000ZZ99` falha dentro de `GPOPBuild()` com `SC2/SM0 nao abertas nesta thread REST`; a correção aguarda recompilação/aplicação via PTM. `MATI650` ainda não está homologado nessa rota.

References:

- `scripts/homologar_totvs_e2e_etapa7a.py` — instrumento dry-run/opt-in da 7A; exige `--send`, `--confirm-test-environment TOTVS_TESTE`, `--confirm-business-op 1079689C001` e `--expected-host ...` para envio real.
- `tests/test_totvs_etapa7a_e2e.py` — teste integrado com ACK controlado.
- `docs/evidencias/TOTVS_ETAPA7A_HOMOLOGACAO_CONTROLADA_2026-09-02.md` — evidência detalhada e separação de estado.
- `ROADMAP.md` — seção `ETAPA 7A — Homologação E2E sem depender do GPOPSYNC real`.
- Comandos validados: `.\.venv\Scripts\python.exe scripts\homologar_totvs_e2e_etapa7a.py`; `.\.venv\Scripts\python.exe -m dotenv run -- .\.venv\Scripts\python.exe -m unittest tests.test_totvs_etapa7a_e2e tests.test_totvs_on_demand tests.test_totvs_outbox tests.test_totvs_operator_queue`; `.\.venv\Scripts\python.exe -m dotenv run -- .\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"`.
- Resultados: teste específico aprovado; conjunto direcionado `115` aprovados; suíte completa `574` aprovados e `1` ignorado; imports principais e UTF-8 aprovados.
