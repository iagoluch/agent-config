thread_id: 01a0c91b-0769-7a11-860c-247008562de3
updated_at: 2026-09-21T17:32:43+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\22\rollout-2026-09-22T09-33-06-01a0c91b-0769-7a11-860c-247008562de3.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Atualização do reset do banco de testes com preservação de OPs fechadas

Rollout context: Projeto em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`. O usuário pediu para reiniciar os dados do banco de teste preservando OPs já fechadas no Protheus.

## Task 1: Alterar o reset para preservar OPs fechadas

Outcome: partial

Preference signals:

- O usuário pediu diretamente: "reinicie os dados do banco teste, menos as OP que ja estão fechadas no protheus" -> em tarefas destrutivas semelhantes, preservar explicitamente os dados identificados como fechados e validar antes de aplicar.

Key steps:

- Foi analisado `scripts/resetar_banco_teste.py`, que limpa tabelas operacionais e remove mensagens `ProductionOrder` da inbox TOTVS.
- O script foi editado para aceitar `--preservar-ops OP1,OP2` e `--preservar-ops-fechadas-protheus`, combinando listas explícitas com OPs descobertas automaticamente.
- A remoção seletiva da tabela `totvs_integration_messages` foi ajustada para não apagar as OPs preservadas.
- Foram mantidas verificações de schema, contagens, dados protegidos, banco real em modo somente leitura e integridade pós-commit.

Failures and how to do differently:

- O reset não foi efetivamente executado nem validado no final; o banco estava com schema 41 enquanto a aplicação esperava 42.
- A conexão ao banco não estava disponível em uma tentativa inicial; não afirmar sucesso sem executar o `--dry-run` e confirmar os resultados.
- O critério apresentado para OP fechada (`status IN ('Concluida', 'Finalizada', 'Fechada')` e `data_finalizacao IS NOT NULL`) aparece como alteração proposta, mas não foi validado contra o schema/dados reais nesta conversa.

Reusable knowledge:

- O script exige confirmação literal do banco para execução real: `--confirmar gestor_pecas_test`.
- O reset preserva estrutura, cadastros/configurações e mensagens TOTVS que não sejam `ProductionOrder`; usa transação, advisory lock, `lock_timeout=5s` e `statement_timeout=60s`.
- A tabela `op_por_tarefa` relaciona tarefas a OPs pelo campo `codigo_op`; `totvs_integration_messages` armazena `transaction`, `external_id`, status e payload bruto.
- Para aplicar migrations, `apply_migrations` precisa receber uma conexão psycopg com `row_factory=dict_row`, não um objeto `PostgresConfig` nem uma conexão com tuplas padrão.

References:

- `scripts/resetar_banco_teste.py`
- `app/database/migrations.py`
- `mes/integrations/totvs/models.py` (`TotvsProductionOrder.number`, `status_order_type`, datas de início/fim)
- Comando funcional: `python -c "import psycopg; from psycopg.rows import dict_row; from app.database.config import load_postgres_config; from app.database.migrations import apply_migrations; config = load_postgres_config(testing=True); with psycopg.connect(config.dsn, row_factory=dict_row) as conn: apply_migrations(conn); print('Migrations aplicadas com sucesso!')"`
- Erros encontrados: `ModuleNotFoundError: No module named 'psycopg'`; `AttributeError: 'PostgresConfig' object has no attribute 'cursor'`; `TypeError: tuple indices must be integers or slices, not str`.
- Próximo passo pendente: executar `python scripts/resetar_banco_teste.py --dry-run --preservar-ops-fechadas-protheus` e só depois considerar a execução confirmada.
