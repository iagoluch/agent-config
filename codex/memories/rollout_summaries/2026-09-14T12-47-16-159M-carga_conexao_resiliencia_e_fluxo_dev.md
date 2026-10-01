thread_id: 01a09ff5-1e48-7f13-8b90-a608f780b9fa
updated_at: 2026-09-14T12:31:07+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-16-01a09ff5-1e48-7f13-8b90-a608f780b9fa.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Conexão, carga, resiliência e fluxo de desenvolvimento foram investigados e parcialmente otimizados

Rollout context: Projeto em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, backend FastAPI/Uvicorn, PostgreSQL via `psycopg_pool`, integrações TOTVS/SigmaNEST e frontend React.

## Task 1: Polimento visual e correções de UI

Outcome: success

Preference signals:
- O usuário pediu revisão visual ampla, não apenas de um print: alinhamento de cards em várias abas, correção do redimensionamento dos botões com PDF e “animações singelas” em popups e transição de abas -> futuras mudanças visuais devem priorizar componentes compartilhados e consistência entre telas.

Key steps:
- Ajustados `web/src/styles/tokens.css` e `web/src/styles/global.css` para sombras/elevação consistentes, hover discreto, cards responsivos e animações de dialogs, drawers, calendário e troca de abas.
- Corrigido o layout dos botões do workbench do operador usando tamanhos fluidos com `clamp()` e proteção contra quebra de texto quando o card PDF ocupa espaço lateral.
- Build de produção passou; testes de management/operator passaram; validação visual foi feita em viewport reduzido, 1400px e 1920px.

Reusable knowledge:
- Os componentes compartilhados (`.section-card`, `.metric-card`, `.resource-card`, `.operator-production-card`) propagam ajustes visuais para várias abas; preferir correções de base em vez de alterações página a página.

## Task 2: Remoção de linguagem técnica da UI

Outcome: success

Preference signals:
- O usuário pediu remover referências visíveis a “backend”, cálculos internos e implementação durante a transição para o TOTVS real -> textos para o usuário devem ser operacionais/de negócio, sem explicar a arquitetura interna.

Key steps:
- Removidas menções técnicas em `PageFrame.tsx`, `AnalyticsPages.tsx`, `HomePages.tsx`, `ReportsPages.tsx` e `QualityInspectionPage.tsx`.
- Comentários internos sobre backend foram preservados porque não aparecem na UI.
- Testes de management/quality e `tsc -b` passaram.

## Task 3: Conexão, transição para banco real e resiliência

Outcome: partial

Key steps:
- Identificada a separação entre PostgreSQL próprio, TOTVS via SOAP/HTTP e SigmaNEST via SQL Server/ODBC.
- Produção foi habilitada em `backend/api/main.py`: `GESTOR_WEB_ENV=production` usa `DATABASE_URL`/configuração produtiva; ambientes `development`/`test` continuam isolados.
- O banco de teste continua protegido por validações de nome/DSN; a cadeia versionada de `app/database/migrations.py` aplica o schema automaticamente.
- Pool PostgreSQL padrão foi aumentado de 4 para 10 conexões, configurável por `PGPOOL_MAX_SIZE`.
- Adicionado `statement_timeout` padrão de 30s via `PGSTATEMENT_TIMEOUT_MS`, timezone de sessão e keepalive PostgreSQL (`keepalives=1`, idle 30s, intervalo 10s, 3 tentativas).
- SigmaNEST recebeu timeout de consulta/execução e a busca de OP sob demanda do TOTVS recebeu uma segunda tentativa apenas para falhas de transporte.
- Testes de configuração, SigmaNEST e TOTVS passaram.

Failures and how to do differently:
- Não adicionar retry genérico em torno de transações PostgreSQL: pode reexecutar efeitos colaterais parcialmente aplicados. Preferir timeout, pool, recuperação controlada e retries apenas em operações idempotentes/transportes classificados.
- O ambiente de preview registra `ModuleNotFoundError: No module named 'pyodbc'` no sync SigmaNEST. O erro é capturado e não derruba a API, mas o driver precisa ser instalado/configurado quando a integração SigmaNEST for necessária.

## Task 4: Teste de carga com 45 operadores

Outcome: success

Key steps:
- Criado `tests/load_test/run_operator_load_test.py`, usando schema PostgreSQL isolado e descartável dentro de `TEST_DATABASE_URL`; o schema é removido ao final e não toca o banco oficial/real.
- A carga simulou 45 operadores e 5 gestores durante 40s, com endpoints de login, contexto, workbench, motivos de parada, ações e dashboards.
- Antes do isolamento do login: 3.458 requisições, 12 conflitos esperados, 0 erros de sistema e 0 respostas 503.
- O gargalo principal foi login: aproximadamente p50 2,1–2,4s e p99 3,8–4,2s, causado pelo custo CPU do PBKDF2 de 600.000 iterações, não por conexão.
- Aumentar o thread pool geral para 100 reduziu latência de endpoints leves; o login permaneceu lento, confirmando gargalo de CPU.
- O login foi isolado em limiter próprio de 8 threads (`GESTOR_WEB_AUTH_THREAD_POOL_SIZE`), preservando a segurança do hash e evitando que logins em massa bloqueiem workbench/contexto.
- Suíte `tests.test_web_api` (49 testes) e `tests.test_ai` (41 testes) passou.

## Task 5: Teste de carga completo com 40 operadores

Outcome: success

Key steps:
- O teste foi ampliado para OPs reais criadas pelo pipeline canônico de ingestão TOTVS, cobrindo `carregar_roteiro`, `Início`, `Parada`, `Retomar`, `Finalizar`, histórico, contexto e workbench.
- Execução: 40 operadores + 5 gestores, 45s, 3.614 requisições, timeout de 15s.
- Nenhuma requisição travou; zero HTTP 5xx, zero 503 e nenhuma exceção não tratada.
- Latências relevantes: `acao_inicio` p50 2,18s/p99 2,99s; login p50 2,17s/p99 3,98s; workbench p50 142ms/p99 747ms; contexto p50 75ms/p99 535ms.
- Erros observados foram recusas esperadas de negócio: `operator_resource_occupied` por compartilhamento deliberado de postos, `primeira_peca_gate_obrigatorio` e `primeira_peca_nao_produzida` por tentativa de finalizar sem Setup/primeira peça.

Reusable knowledge:
- O script de carga deve classificar erros por HTTP/status/código, distinguindo recusas de regra (`409/403/422`) de falhas de infraestrutura (`5xx/503`). Não tratar todo erro de ação como defeito.
- O teste usa recursos reais do catálogo; com 40 operadores e menos postos físicos, conflitos de ocupação são esperados e úteis para validar concorrência.

## Task 6: Travamento da porta 8001 e acúmulo ao longo do tempo

Outcome: success

Key steps:
- Diagnóstico confirmou que o processo Python antigo na porta 8001 estava travado: `curl` não recebeu resposta em 8s para `/` nem `/api/v1/system/health`.
- O processo foi encerrado e a porta ficou livre; o servidor foi reiniciado e a tela de login voltou a carregar.
- O principal risco durável identificado foi conexão PostgreSQL meio-morta sem keepalive, capaz de deixar uma requisição pendurada após queda de rede/VPN/hibernação. Keepalive foi adicionado à configuração DSN.
- O servidor 8001 passou a usar `uvicorn --reload`, observando apenas `app`, `backend` e `mes`; logs confirmaram “Started reloader process ... using WatchFiles”.
- Alterações Python nessas pastas agora reiniciam automaticamente em desenvolvimento. Alterações em `web/src` ainda exigem `npm run build` para atualizar o `web/dist` servido pela API; a API não precisa ser reiniciada para cada build frontend.

Failures and how to do differently:
- O processo antigo não respondia, mas não havia evidência de vazamento de memória; os buffers de observabilidade têm `deque(maxlen=...)` e o broker SSE remove assinantes ao desconectar.
- O sync SigmaNEST continua gerando stack trace controlado quando `pyodbc` não está instalado. Isso não impede o login/API, mas gera ruído nos logs e deve ser resolvido instalando o driver ou desabilitando o sync nesse ambiente.

References:
- `tests/load_test/run_operator_load_test.py` — teste de carga isolado e reutilizável.
- `tests/load_test/last_run_report.json` — métricas da última execução.
- `app/database/config.py` — pool, timeouts, keepalive e DSN.
- `app/database/connection.py` — pool PostgreSQL e configuração de sessão.
- `backend/api/main.py` — ambiente produtivo, limiter de threads e lifespan.
- `backend/api/config.py` — `GESTOR_WEB_THREAD_POOL_SIZE` e `GESTOR_WEB_AUTH_THREAD_POOL_SIZE`.
- `backend/api/routers/auth.py` — login assíncrono e fila dedicada para PBKDF2.
- `.claude/launch.json` — configuração atual do servidor 8001 com `--reload`.
- Evidência do teste de 40 operadores: “Total: 3614 requisições”, “Nenhuma ação travou”, “Nenhum 5xx / erro interno”.
