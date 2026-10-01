thread_id: 01a09ff5-212f-7940-8453-3a15471433db
updated_at: 2026-09-08T15:36:05+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-17-01a09ff5-212f-7940-8453-3a15471433db.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 3 foi concluída após correção de concorrência e validação final

Rollout context: Projeto Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, com PostgreSQL TESTE `gestor_pecas_test`, SigmaNEST somente leitura e nenhuma movimentação produtiva real no TOTVS.

## Task 1: Fechamento da Wave 3 e correção do fluxo on-demand TOTVS

Outcome: success

Preference signals:
- O usuário pediu explicitamente para “não recomeçar a Wave 3”, não refazer funcionalidades concluídas e usar o estado atual como fonte de verdade -> futuras intervenções devem começar pelo ponto pendente e respeitar alterações pós-Wave 3.
- O usuário exigiu que a duplicação do Andon fosse investigada na causa real, sem apenas relaxar os testes -> a correção deve preservar a regra de um recurso físico por cartão e validar backend, API, transformação e renderização.
- O usuário reforçou: “Não iniciar homologação manual de apontamentos. Não iniciar Wave 4. Apenas fechar corretamente a Wave 3.” -> após validação, encerrar sem expandir escopo.

Key steps:
- A falha inicial do Andon deixou de reproduzir: `web/src/test/andon.test.tsx` passou com 13/13; a suíte frontend passou posteriormente com 79/79.
- A suíte backend completa foi executada após as alterações em fakes/fixtures e terminou com 680 testes OK e 1 skip previsto.
- A falha intermitente encontrada sob carga em `tests.test_totvs_on_demand` foi reproduzida e isolada: um seguidor consultava uma OP no intervalo em que o líder já havia criado o cabeçalho, mas ainda não havia materializado o roteiro; isso retornava incorretamente `sem_roteiro`.
- O fluxo foi corrigido para que “cabeçalho sem roteiro” não seja terminal quando existe solicitação `PENDING`; o seguidor espera dentro do timeout e não dispara uma segunda chamada ao TOTVS. Quando não há sincronização em curso, `sem_roteiro` continua sendo retornado legitimamente.
- O módulo on-demand passou isoladamente com 39/39, e a corrida foi coberta por testes determinísticos adicionais.
- `npx tsc -b` terminou com exit 0; `npm run build` terminou com sucesso. Houve apenas o aviso não bloqueante de chunk maior que 500 KB.
- As verificações diretas confirmaram `gestor_pecas_test` no schema 24 e `gestor_pecas` REAL no schema 11.
- `qlik/` não existe na raiz; o único arquivo de integração SigmaNEST com SQL é `backend/integrations/sigmanest_sqlserver.py`, que contém zero ocorrências executáveis de INSERT/UPDATE/DELETE/MERGE.
- A inspeção visual foi realizada em preview isolado: Corte, Destaque, apontamento normal, Qualidade/bypass e Pausas. As capturas reportaram `overflowX: false`; a evidência foi arquivada em `docs/evidencias/wave3/`.
- `AGENTS.md` e `ROADMAP.md` foram atualizados com o estado implementado, schema, autoridade do Gestor, sincronização Corte, Destaque por plano, bypass transitório da Qualidade, pausas configuráveis, remoção do Qlik e pendências externas.

Failures and how to do differently:
- A execução completa inicialmente terminou com 678 OK e 1 falha intermitente (`sem_roteiro` vs `sincronizada`), embora o módulo isolado passasse repetidamente. O problema era uma janela de corrida real entre cabeçalho e roteiro, não um teste instável; futuras mudanças no on-demand devem considerar explicitamente o estado `PENDING` antes de classificar uma OP como sem roteiro.
- A primeira execução da suíte frontend apresentou 1 falha intermitente sob carga; a reexecução passou 79/79. Ainda assim, o resultado final deve ser baseado na execução verde completa, não na primeira tentativa.

Reusable knowledge:
- A marca d’água SigmaNEST é baseada na maior `data_programa` materializada menos 7 dias (`DEFAULT_OVERLAP_DAYS = 7`); a projeção é incremental e idempotente.
- O Corte usa o mesmo `SigmaNestRefreshCoordinator` para ciclo automático e botão “Atualizar tarefas”, serializado por `asyncio.Lock`; falhas preservam a última fila local.
- O Destaque é agrupado por tarefa e plano/chapa; uma chapa cortada pode aparecer imediatamente, com situação PARCIAL/COMPLETA, sem assumir que um nesting equivale a uma única chapa.
- A dispensa de Qualidade usa status `DISPENSADA`, crachá e auditoria, sem apontamento, template, aprovação, cota ou RNC; `ck_qualidade_inspecao_dispensa` impede falsificação.
- A origem da fila da Qualidade é a última etapa apontável anterior à inspeção; uma OP de outro setor deve resultar em `qualidade_op_outro_setor`.
- Pausas automáticas são configuradas em `pausas_automaticas_setor`; a configuração inicial preserva Almoço 12:10–12:52 e Café 15:30–15:45 para os nove setores.
- A composição visual do Andon pós-ajustes usa colunas independentes, cartões uniformes por token/resolução, um cartão por recurso/estação e animações distintas para entrada e mudança de estado.

References:
- `mes/integrations/totvs/on_demand.py`: correção do lookup pré-reserva e espera do seguidor durante `PENDING`.
- `tests/test_totvs_on_demand.py`: testes determinísticos da janela de corrida e preservação do caso real sem roteiro.
- `web/src/test/andon.test.tsx`: 13 testes verdes após a correção do Andon.
- `mes/services/sigmanest_refresh.py`: coordenação automática/manual, estado observável e mensagens sem detalhes técnicos.
- `backend/api/routers/cutting.py`: `POST /cutting/sync`, `GET /cutting/sync/diagnostico` e estado de última sincronização.
- `app/database/schema.py`: `SCHEMA_VERSION = 24`.
- Comandos finais validados: `.venv/Scripts/python.exe -m unittest discover -s tests` → `Ran 680 tests ... OK (skipped=1)`; `npx vitest run` → `79 passed`; `npx tsc -b` → exit 0; `npm run build` → sucesso.
- `docs/evidencias/wave3/`: capturas visuais arquivadas das telas alteradas.
