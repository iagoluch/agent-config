---
name: procedimento-explain-banco-descartavel
description: "Auditoria que exige EXPLAIN/carga com banco de teste vazio: criar banco descartável semeado (5 passos) em vez de declarar 'não testado'."
metadata:
  node_type: memory
  type: reference
  originSessionId: 6ec46f4d-d3d4-4db7-bead-448e103dba7f
  modified: 2026-09-29T13:10:46.375Z
---

Quando um checklist pede `EXPLAIN (ANALYZE, BUFFERS)` ou ensaio de carga e o banco de teste está vazio
(caso real 28/09/2026: TEST com 1 apontamento, banco de simulação de 3 meses com 0 linhas em 62 tabelas):

1. Criar banco **descartável** com sufixo contendo "test" (satisfaz a trava de `Database.__init__`) e
   `GESTOR_EXPECTED_DATABASE` apontando para ele.
2. Aplicar schema com `app.database.migrations.apply_migrations` via `Database(config=PostgresConfig(dsn))` —
   nunca schema à mão.
3. Semear com `generate_series` respeitando CHECKs e índices únicos parciais; deixar o semeador forçar cada
   INSERT até passar é mais barato que ler as 51 migrations.
4. Medir com `EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)` e a app real via `httpx.ASGITransport` (exercita threadpool
   do anyio e pool do psycopg de verdade).
5. Dropar o banco no fim; reportar volume como **sintético** e extrapolação como estimativa.

**Why:** sem volume, todo EXPLAIN é seq scan de 0 linhas; foi assim que se provou o pool de 4 conexões
esgotado por telas gerenciais (503 medido) — relatório em docs/auditoria_backend_2026-09-25/.
**How to apply:** em qualquer auditoria de performance/pool neste repo, checar volume antes; se vazio, seguir os 5 passos.
