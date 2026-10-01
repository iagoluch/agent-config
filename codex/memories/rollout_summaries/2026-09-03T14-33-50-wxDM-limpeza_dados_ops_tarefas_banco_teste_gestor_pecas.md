thread_id: 01a067b0-bb43-7842-b13b-89acfefee236
updated_at: 2026-09-03T14:37:45+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\03\rollout-2026-09-03T11-33-50-01a067b0-bb43-7842-b13b-89acfefee236.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Limpeza seletiva concluída no banco PostgreSQL de teste, preservando estrutura e dados protegidos

Rollout context: No projeto `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, o usuário pediu em português: “Limpe os dados (OPs, tarefas) do banco teste”. O trabalho foi realizado em PowerShell usando Python 3.14, psycopg e as proteções existentes da aplicação.

## Task 1: Limpar OPs, tarefas e dados relacionados somente no banco de teste

Outcome: success

Preference signals:

- O usuário pediu limpeza de dados de OPs e tarefas, não remoção da estrutura do banco -> em tarefas semelhantes, preservar tabelas, migrations, índices e constraints; usar limpeza de dados, não `DROP TABLE`.
- A operação foi explicitamente limitada ao banco de teste -> confirmar o DSN efetivo antes de qualquer ação destrutiva e manter uma barreira adicional com `GESTOR_EXPECTED_DATABASE`.
- A limpeza deveria abranger dados relacionados às OPs/tarefas, mas não configurações e dados administrativos -> separar tabelas-alvo de tabelas protegidas e validar ambas antes/depois.

Key steps:

- A configuração foi carregada com `testing=True` e `GESTOR_EXPECTED_DATABASE=gestor_pecas_test`. A conexão real confirmou banco `gestor_pecas_test`, usuário `gestor_app`, porta local `15432` e schema 20.
- Foi feito levantamento prévio das contagens e dependências do schema. Antes da limpeza havia 42 OPs no catálogo, 17 tarefas, 34 vínculos OP–tarefa, 58 apontamentos operacionais, 53 apontamentos de corte, 732 operações SigmaNEST, 224 planos de corte e outros eventos relacionados.
- O banco real foi conectado separadamente em modo somente leitura antes da exclusão, confirmando `gestor_pecas` com 7 tarefas e 4.542 OPs.
- Em uma transação, foram truncadas com `RESTART IDENTITY` as tabelas de planejamento/execução e seus dados derivados, incluindo `tarefas`, `op_por_tarefa`, catálogos PCP/SIGMANEST, apontamentos, eventos operacionais, histórico, sincronizações e tabelas TOTVS relacionadas.
- Foram removidos seletivamente os 3 envelopes `ProductionOrder` de `totvs_integration_messages`; as 5 mensagens `WhoIs` foram preservadas.
- A validação exigiu que todas as tabelas-alvo ficassem com zero registros e que as tabelas protegidas mantivessem exatamente as mesmas contagens. A transação foi então confirmada.

Reusable knowledge:

- `app/database/config.py`, `load_postgres_config(testing=True)`, exige `TEST_DATABASE_URL`, rejeita o mesmo DSN de produção, exige que o nome do banco contenha `test` e suporta `GESTOR_EXPECTED_DATABASE` para conferência exata.
- O alvo validado nesta execução foi `127.0.0.1:15432`, database `gestor_pecas_test`; o banco real no mesmo endpoint foi `gestor_pecas`.
- Tabelas protegidas nesta operação: `usuarios`, `schema_migrations`, `catalogo_recursos_pcfactory`, `catalogo_status_recursos`, `calendarios_produtivos`, `turnos_produtivos`, `intervalos_turno_produtivo`, `ai_conversations`, `ai_messages` e `generated_reports`.
- A estratégia segura validada é: confirmar DSN e banco atual; enumerar/contar tabelas; separar protegidas e elegíveis; usar `TRUNCATE ... RESTART IDENTITY` dentro de transação; remover apenas envelopes TOTVS explicitamente elegíveis; comparar contagens antes/depois; confirmar o banco real em modo read-only.

Failures and how to do differently:

- Uma busca ampla com `rg` usando `.env*` e `docker-compose*.yml` produziu erro de sintaxe do Windows (`os error 123`); em PowerShell, evitar esses padrões globais diretamente ou pesquisar arquivos explicitamente. Isso não afetou a limpeza.
- O resultado intermediário informou 2.538 linhas truncadas; somando os 3 envelopes `ProductionOrder` removidos, o total final corretamente reportado foi 2.541 registros. Em futuras respostas, distinguir claramente linhas truncadas de exclusões seletivas para evitar ambiguidade.
- Não inferir que o diretório do projeto identifica um banco seguro. Sempre confirmar o nome retornado por `current_database()` e comparar com `GESTOR_EXPECTED_DATABASE` antes de executar SQL destrutivo.

References:

- Diretório de trabalho: `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`
- Configuração: `app/database/config.py`, função `load_postgres_config`
- Schema: `app/database/migrations.py`, schema version 20 nesta execução
- Comando de proteção usado: `$env:GESTOR_EXPECTED_DATABASE='gestor_pecas_test'; ... load_postgres_config(testing=True) ... SELECT current_database()`
- Resultado final do teste: `TEST_FINAL ('gestor_pecas_test', 0, 0, 12, 20)`
- Resultado final da produção: `PRODUCTION_FINAL ('gestor_pecas', 7, 4542, 11, 11)`
- Validação dos dados protegidos: usuários `12 → 12`; schema migrations `20 → 20`; recursos `382 → 382`; status `84 → 84`; calendários `1 → 1`; turnos `6 → 6`; intervalos `4 → 4`; conversas IA `1 → 1`; mensagens IA `5 → 5`; relatórios `2 → 2`.
- Resultado final comunicado ao usuário: OPs `42 → 0`, tarefas `17 → 0`, vínculos `34 → 0`, `ProductionOrder` `3 → 0`, `WhoIs` preservadas `5`, banco real inalterado com 7 tarefas e 4.542 OPs.
