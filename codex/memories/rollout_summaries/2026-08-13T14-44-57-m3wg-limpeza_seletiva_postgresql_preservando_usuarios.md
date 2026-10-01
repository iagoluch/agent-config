thread_id: 019ffb95-5dcb-7cf3-a43e-84248b78500c
updated_at: 2026-08-13T14:48:14+00:00
rollout_path: C:\Users\logistica.unidade4\.codex\sessions\2026\08\13\rollout-2026-08-13T11-44-58-019ffb95-5dcb-7cf3-a43e-84248b78500c.jsonl
cwd: \\?\C:\Users\logistica.unidade4\Documents\Sistema - Iago\Gestor de Peças - Area de Testes
git_branch: main

# Limpeza seletiva do banco PostgreSQL para novo teste, preservando usuários e estrutura

Rollout context: No projeto `C:\Users\logistica.unidade4\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, o usuário pediu para apagar os dados do banco sem excluir tabelas nem registros da tabela `usuarios`.

## Task 1: Limpar dados do banco sem remover usuários ou tabelas

Outcome: success

Preference signals:

- O usuário especificou inicialmente: “formate as informações de tudo do banco de dados, menos os usuarios (não é para excluir as tabelas, só os dados dele)” e depois reforçou: “só limpar os dados, não as tabelas, não os usuarios” -> em operações destrutivas semelhantes, preservar explicitamente a tabela `usuarios` e sua carga, além de manter toda a estrutura do banco.
- O usuário queria repetir os testes com o banco limpo, não recriar o schema -> manter migrations, índices, constraints e tabelas intactos.

Key steps:

- O projeto foi inspecionado para localizar a configuração PostgreSQL e as tabelas. `DATABASE_URL` apontava para `gestor_pecas`; não havia `TEST_DATABASE_URL` configurada.
- A operação foi inicialmente bloqueada para confirmação porque o único banco disponível era identificado como operacional, não como banco de testes.
- Após a confirmação do usuário, foi executada uma transação que:
  - protegeu `usuarios` e `schema_migrations`;
  - enumerou as tabelas públicas existentes;
  - contou os registros antes da limpeza;
  - executou `TRUNCATE TABLE ... RESTART IDENTITY` apenas nas 11 tabelas elegíveis;
  - verificou as contagens após a limpeza;
  - confirmou a transação.
- Resultado validado: 78.241 registros removidos; todas as 11 tabelas de dados ficaram com zero registros; 8 usuários foram preservados; `schema_migrations` foi preservada.

Failures and how to do differently:

- Não havia banco de teste isolado: `TEST_DATABASE_URL` estava ausente. A limpeza só foi feita depois de informar que o alvo seria o banco operacional `gestor_pecas` e obter confirmação explícita.
- Em futuras limpezas, nunca inferir que o banco é seguro apenas pelo diretório do projeto; verificar a DSN, bloquear se não houver `TEST_DATABASE_URL` isolada e pedir confirmação antes de qualquer comando destrutivo.
- Não usar `DROP TABLE` nem truncar `usuarios` ou `schema_migrations`; a checagem de existência das tabelas protegidas deve ocorrer antes da limpeza.

Reusable knowledge:

- A configuração em `app/database/config.py` usa `DATABASE_URL` para operação normal e exige explicitamente `TEST_DATABASE_URL` quando `testing=True`; testes não fazem fallback para o banco operacional.
- O schema PostgreSQL do projeto inclui as tabelas `tarefas`, `op_por_tarefa`, `historico`, `usuarios`, `eventos_sistema`, `schema_migrations`, `apontamentos_operacionais`, tabelas de catálogo PCP/SIGMANEST, `catalogo_sigmanest_planos_corte` e `apontamentos_corte`.
- A estratégia validada para reset de dados é truncar somente as tabelas não protegidas com reinício das identidades, dentro de transação, e conferir contagens antes/depois.

References:

- Configuração: `app/database/config.py`, função `load_postgres_config(testing=False|True)`.
- Schema/tabelas: `app/database/migrations.py`, `EXPECTED_TABLES`, `SCHEMA_VERSION = 3`.
- Destino identificado: `database=gestor_pecas`; configuração operacional em `127.0.0.1:15432`; conexão PostgreSQL efetiva reportou `172.18.0.2/32:5432`.
- Tabelas limpas: `apontamentos_corte`, `apontamentos_operacionais`, `catalogo_pcp_ops`, `catalogo_sigmanest_ops`, `catalogo_sigmanest_planos_corte`, `catalogo_sigmanest_programas`, `catalogo_sigmanest_tarefas`, `eventos_sistema`, `historico`, `op_por_tarefa`, `tarefas`.
- Verificação final: cada tabela limpa = `0`; `usuarios_preservados = 8`; `schema_migrations: preservada`.
