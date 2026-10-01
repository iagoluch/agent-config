---
id: 2
title: "Pedido de EXPLAIN em banco de teste vazio exige criar banco descartavel semeado"
status: actioned
type: internal
skill: []
target_file: []
siblings_checked: "task-observer: instancia - insight especifico de projeto, sem propagacao"
area: "protocolo de auditoria de performance e dados quando o banco de teste esta sem volume"
date: 2026-09-28
session_context: "Auditoria total do backend do Gestor de Pecas (mes/domain, mes/analytics, mes/services, backend/api, app/database) com exigencia de EXPLAIN (ANALYZE, BUFFERS) e ensaio de carga em TEST"
parked_until: 
resolved: 2026-09-29
resolution: "Sem skill-alvo; virou memória do projeto procedimento-explain-banco-descartavel.md (decisão do usuário na revisão)"
reference: "docs/auditoria_backend_2026-09-25/RELATORIO.md"
---

**Issue:** o pedido de auditoria exigia "Queries criticas: EXPLAIN (ANALYZE, BUFFERS) em TEST"
e "Carga: p50/p95/p99, throughput, pool wait e erros". Ao abrir o ambiente, o banco de teste
principal tinha 1 apontamento operacional e o banco de simulacao de 3 meses estava com 0 linhas
em todas as 62 tabelas - provavelmente volume de um simulador que rodou em outra maquina e nao
foi materializado aqui. Com tabelas vazias, todo EXPLAIN e um seq scan de 0 linhas e o ensaio de
carga so mediria o overhead do HTTP. Sem volume, a auditoria de performance e de exaustao de pool
teria de ser declarada "NAO TESTADA" e o achado mais grave do sistema (pool de 4 conexoes
esgotado por telas gerenciais, com 503 medido) ficaria sem prova.

**Suggested improvement:** quando o checklist de auditoria exigir medicao de query ou carga e o
banco de teste estiver vazio, o procedimento a seguir e: (1) criar um banco **descartavel**
separado, com sufixo que contenha "test" para satisfazer a trava de `Database.__init__`, e
`GESTOR_EXPECTED_DATABASE` apontando para ele; (2) aplicar o schema com o proprio
`app.database.migrations.apply_migrations` via `Database(config=PostgresConfig(dsn))`, para nao
divergir do schema real; (3) semear com `generate_series` respeitando os CHECKs e os indices
unicos parciais do schema real - os CHECKs sao ons e ensinam a forma correta das colunas, entao
deixar o semeador forcar cada INSERT ate passar e mais barato que ler 51 migrations; (4) medir
com `EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)` e com a app real via `httpx.ASGITransport`, que
exercita o threadpool do anyio e o pool do psycopg de verdade, e nao um mock; (5) remover o banco
no fim e reportar o volume como volume **sintetico**, com a extrapolacao marcada como estimativa,
nunca como fato de producao.

**Principle:** um checklist de auditoria que pede medicao tem uma pre-condicao silenciosa - a
existencia de dados representativos no ambiente de teste. Quando a pre-condicao falta, a resposta
nao e pular a medicao nem declarar "NAO TESTADO" por conveniencia: e **construir a pre-condicao
de forma descartavel e rastreavel**, marcando com honestidade o que aquele volume representa e o
que ele nao representa. A prova vale pelo que ela isola, nao pelo absoluto do numero - e um banco
semeado e destruido e preferivel a um achado sem prova.
