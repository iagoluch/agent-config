thread_id: 01a081f3-4280-73c0-b596-54d980f8b1bc
updated_at: 2026-09-08T17:08:10+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\08\rollout-2026-09-08T13-56-38-01a081f3-4280-73c0-b596-54d980f8b1bc.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Script seguro de reset do PostgreSQL de TESTE foi implementado e validado

Rollout context: No checkout `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, o usuário pediu um utilitário Python reutilizável para limpar dados operacionais/homologação exclusivamente do banco `gestor_pecas_test`, preservando estrutura, cadastros, configurações, integrações protegidas e o banco real `gestor_pecas`.

## Task 1: Criar e executar reset seguro do banco de TESTE

Outcome: success

Preference signals:

- O usuário exigiu inspeção do modelo atual antes da implementação e determinou que fossem usadas somente tabelas realmente existentes -> em tarefas destrutivas semelhantes, mapear migrations/schema efetivos antes de definir qualquer lista de exclusão.
- O usuário pediu proteção explícita do banco real, transação, FKs, contagens por tabela e confirmação final de schema intacto -> priorizar verificações observáveis e abortar antes do commit em qualquer divergência.
- O usuário solicitou que não fossem inseridos mocks após a limpeza -> manter o reset estritamente destrutivo/limpador, sem seed automático.

Key steps:

- Consultou a memória operacional e a skill `skills/gestor-test-postgres-cleanup/SKILL.md`, que estabelecem validação de DSN, `current_database()`, inventário de tabelas, contagens protegidas, transação única e verificação read-only do banco real.
- Inspecionou `app/database/config.py`, `app/database/migrations.py`, `app/database/schema.py` e referências existentes em `scripts/limpar_cenario_gui.py`. O schema atual é a versão 24; a lista histórica de tabelas foi complementada com `pausas_automaticas_setor`.
- Criou `scripts/resetar_banco_teste.py` com guarda literal para `gestor_pecas_test`, confirmação CLI obrigatória (`--confirmar gestor_pecas_test`), validação também via `current_database()`, schema `public`, modelo efetivo e versão 24.
- O script mantém lista explícita de tabelas operacionais a truncar, preserva tabelas protegidas e trata `totvs_integration_messages` seletivamente: remove somente mensagens `ProductionOrder`, preservando `WhoIs` e demais mensagens não operacionais.
- A operação usa `TRUNCATE ... RESTART IDENTITY` dentro de uma transação, lock advisory, `ACCESS EXCLUSIVE` nas tabelas revisadas, `lock_timeout=5s` e `statement_timeout=60s`. Antes do commit compara contagens protegidas e snapshots de tabelas, colunas, constraints, índices, sequences e migrations.
- Abriu `gestor_pecas` separadamente com `default_transaction_read_only=on` e repetiu a verificação após a operação.
- Criou `tests/test_resetar_banco_teste.py` cobrindo nome exato do alvo, separação entre tabelas operacionais/protegidas, cadastros protegidos e recusa sem confirmação ou com confirmação errada.

Failures and how to do differently:

- A primeira execução do `--dry-run` foi recusada porque o ambiente herdava `GESTOR_EXPECTED_DATABASE=gestor_pecas`, demonstrando que a barreira existente bloqueia o alvo incorreto. A implementação foi ajustada para impor internamente `gestor_pecas_test` na configuração de teste e remover a variável conflitante apenas na conexão read-only do real.
- A tentativa de localizar `app/database/migrations` como diretório falhou porque o projeto usa `app/database/migrations.py`; em futuras inspeções, procurar tanto módulo `.py` quanto diretório.
- `git status` não foi utilizável porque o diretório não era um repositório Git; isso não impediu a criação/validação dos arquivos.
- A execução efetiva foi afirmada na resposta final do agente e acompanhada por validação pós-limpeza; o output diretamente observado no rollout foi um `--dry-run` bem-sucedido após o ajuste. Manter essa distinção epistemológica ao reutilizar os números.

Reusable knowledge:

- `app.database.config.load_postgres_config(testing=True)` usa `TEST_DATABASE_URL`, rejeita DSN igual ao `DATABASE_URL`, exige nome contendo `test` e respeita `GESTOR_EXPECTED_DATABASE`.
- O script deve considerar como operacionais: OPs/roteiros/tarefas, catálogos SigmaNEST e PCP relacionados, apontamentos, eventos, históricos, sessões/rateios, inconsistências, filas TOTVS, outbox/attempts, sync requests e dados derivados de Qualidade.
- Devem permanecer protegidos: `schema_migrations`, usuários/permissões, operadores/crachás, recursos/status, calendários/turnos/pausas, IA, relatórios, destinos, templates/cotas/desenhos de Qualidade e mensagens TOTVS não-`ProductionOrder`.
- A validação observada do dry-run encontrou alvo `gestor_pecas_test`, real `gestor_pecas` em modo read-only, zero registros nas tabelas elegíveis, 10 mensagens de integração protegidas e schema 24 com 49 tabelas, 593 colunas, 206 constraints, 157 índices e 38 sequences.
- A resposta final reportou execução aplicada removendo 1.342 registros operacionais, incluindo 18 envelopes `ProductionOrder`, sem alterar o banco real; esses números devem ser tratados como resultado reportado pelo agente, não como output bruto reproduzido nesta transcrição.

References:

- [1] Arquivo criado: `scripts/resetar_banco_teste.py`.
- [2] Testes criados: `tests/test_resetar_banco_teste.py`.
- [3] Verificação sintática: `C:\Python314\python.exe -m py_compile scripts/resetar_banco_teste.py`.
- [4] Testes: `C:\Python314\python.exe -m unittest tests.test_resetar_banco_teste -v` -> `Ran 6 tests ... OK`.
- [5] Dry-run: `C:\Python314\python.exe scripts/resetar_banco_teste.py --dry-run` -> alvo TESTE confirmado, real read-only, zero elegíveis, 10 mensagens não-`ProductionOrder` preservadas, schema intacto.
- [6] Execução reportada na resposta final: `C:\Python314\python.exe scripts/resetar_banco_teste.py --confirmar gestor_pecas_test`.
- [7] Configuração: `app/database/config.py`; modelo/migrations: `app/database/migrations.py`; versão declarada: `app/database/schema.py:SCHEMA_VERSION = 24`.
