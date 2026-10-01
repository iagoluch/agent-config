thread_id: 01a0825d-4dde-76e0-9ba5-bba95403b10d
updated_at: 2026-09-08T19:43:41+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\08\rollout-2026-09-08T15-52-27-01a0825d-4dde-76e0-9ba5-bba95403b10d.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 4 foi parcialmente implementada; promoção do banco REAL foi corretamente interrompida antes de qualquer escrita insegura

Rollout context: No checkout `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, o usuário pediu a execução da Wave 4 conforme o prompt e depois autorizou explicitamente atualizar o banco REAL para o schema mais novo baseado no TESTE. O PDF `C:\Users\iago.luchtenberg\Documents\Teste fluxo de apontamento.pdf` foi lido e confirmou os mesmos bugs do prompt. O usuário sinalizou urgência com “8% de uso restante”, “3%” e “1%!!!!!!!!!!!!!!!!!”, levando ao encerramento imediato.

## Task 1: Implementação funcional da Wave 4

Outcome: partial

Preference signals:

- O usuário pediu inicialmente apenas “Siga o prompt” e forneceu um documento extenso com a regra de trabalhar somente no TESTE, preservar integrações canônicas, não tocar no REAL sem autorização e não iniciar o cenário completo de fábrica -> em tarefas semelhantes, seguir estritamente a wave solicitada, distinguir instruções do documento da autorização do usuário e não ampliar o escopo.
- O usuário depois disse “atualize o banco real do sistema para o schema mais novo baseado no teste” -> isso foi uma autorização explícita para evolução estrutural do REAL, mas não para copiar dados de TESTE nem executar movimentações produtivas.
- Ao sinalizar consumo crítico de contexto (“8%”, “3%”, “1%!!!!!!!!!!!!!!!!!”), o usuário indicou que a prioridade era encerrar rapidamente com estado comprovado, não continuar investigação ou forçar operações arriscadas.

Key steps:

- O prompt e o PDF foram lidos; o PDF confirmou casos envolvendo T3528/T3539, Laser/Plasma, Destaque, Parada, Retrabalho, finalização parcial, refugo consumindo saldo, override para Qualidade e dez estações de Solda.
- O banco efetivo foi confirmado como `gestor_pecas_test`, schema 24; o REAL `gestor_pecas` permaneceu em schema 11 e foi somente lido.
- O agente implementador alterou domínio, serviços, API, frontend, esquema/migrations e testes para Wave 4.
- Foi criada a migration 25, mas ela não foi aplicada.

Reusable knowledge:

- A regra canônica implementada é `Atendido = Boas + Refugo`; refugo consome saldo sem ser convertido em peça boa, e retrabalho pendente permanece separado.
- Finalização parcial agora encerra o contexto produtivo e retorna a OP para `Aguardando`/fila, preservando saldo e atualização temporal.
- Override de etapa passou a ser persistido para permitir avanço válido para a próxima etapa/Qualidade.
- Exclusividade de recurso foi generalizada para todos os setores; um recurso ocupado não pode receber segundo apontamento concorrente.
- O frontend de Parada preserva o contexto ativo da OP/operação, em vez de convertê-lo indevidamente em parada sem OP.
- Retrabalho/Setup respeita o estado de retorno canônico e não oferece início normal enquanto o retrabalho estiver ativo.
- Destaque foi restringido canonicamente ao Laser Ensis; Plasma permanece no histórico de Corte, mas não libera Destaque.
- Destaque recebeu validações de tarefa completa versus plano individual, idempotência e filtro reversível.
- Histórico do Corte foi reorganizado por nesting, com tarefa, programa, chapa/repetição, máquina, OPs, quantidades, timestamps disponíveis, duração e estado.
- Andon de Corte passou a receber contexto de tarefa/programa/chapa/repetição do apontamento ativo.
- Formatação de medidas remove caudas artificiais de ponto flutuante sem alterar o valor persistido.
- Foram criados dez perfis fixos de Solda (`operador_solda_estacao_1` a `operador_solda_estacao_10`) sobre o mecanismo existente, com recurso fixo e sem seletor manual quando o perfil tem recurso único.
- A auditoria SigmaNEST encontrou campos de programa como `PostDateTime`/`CompDate`, mas não encontrou registros comprobatórios de criação/última atualização para T3528/T3539. Não foi usado `created_at` local como substituto.

Failures and how to do differently:

- A Wave 4 não pode ser declarada concluída: os testes Web ainda têm 5 falhas de expectativas antigas; a suíte PostgreSQL pós-migration, validação visual manual e homologação manual não foram executadas.
- As cinco falhas Web envolvem seleção manual de recurso/Solda removida, bloqueio correto de tarefa Destaque parcial e mudança do histórico para uma linha por nesting. Atualizar os contratos antes de concluir.
- A migration 25 foi criada, mas não validada/aplicada no TESTE. Nunca promover o REAL enquanto a migration não passar no TESTE e nas verificações estruturais.
- A associação dos logins reais às dez estações físicas está bloqueada por falta de dado confiável; não adivinhar o vínculo.
- Datas reais de criação/última atualização da tarefa SigmaNEST estão bloqueadas por dado; não inventar datas locais.

References:

- Arquivos principais: `mes/domain/manufacturing_rules.py`, `mes/services/operator_flow.py`, `mes/services/production.py`, `mes/services/cut.py`, `mes/services/andon.py`, `app/database/database.py`, `app/database/migrations.py`, `app/database/schema.py`, `backend/api/routers/operator.py`, `backend/api/routers/highlight.py`, `web/src/pages/operator/WorkbenchPage.tsx`, `web/src/pages/operator/CuttingPage.tsx`, `web/src/pages/operator/HighlightPage.tsx`, `web/src/utils/format.ts`.
- PDF confirmado: `C:\Users\iago.luchtenberg\Documents\Teste fluxo de apontamento.pdf`.
- Diagnóstico do agente: backend direcionado `54/54` passou; build React/TypeScript/Vite passou com 389 módulos; testes Web `41 passaram, 5 falharam`.

## Task 2: Pedido de promoção do banco REAL

Outcome: partial

Preference signals:

- Quando autorizou “atualize o banco real do sistema para o schema mais novo baseado no teste”, o usuário aceitou promoção estrutural, mas o fluxo seguro deveria continuar exigindo preflight, backup restaurável, aplicação pelas migrations canônicas e validação pós-migration.
- Diante do limite de contexto, o usuário preferiu interrupção imediata a uma operação incompleta ou arriscada; o agente confirmou que nenhuma nova ação seria executada.

Key steps:

- O runbook existente cobria promoção segura do REAL de schema 11 para 19 e exigia parar escritores, confirmar sessões, executar auditoria read-only, gerar/validar `pg_dump -Fc`, aplicar migrations pela aplicação e realizar smoke tests.
- Como a Wave 4 introduziu a migration 25 e ela ainda não havia sido aplicada/validada no TESTE, a promoção 11→25 foi corretamente considerada insegura.
- Nenhum backup do REAL foi iniciado; nenhuma migration foi executada no REAL; nenhum dado de TESTE foi copiado; nenhuma movimentação produtiva ou chamada transacional ao TOTVS ocorreu.

Failures and how to do differently:

- Não tratar “autorização para atualizar o REAL” como autorização para pular gates. Primeiro aplicar e validar a migration 25 em `gestor_pecas_test`, atualizar testes quebrados, executar preflight completo 11→25, criar e restaurar backup verificável e só então promover.
- O rollout terminou com o REAL intacto em schema 11. O status correto é promoção não iniciada/parcial, não sucesso.

Reusable knowledge:

- O workspace não possui metadados Git confiáveis (`NO_GIT_METADATA`/`git status` falhou); controlar alterações por inventário de arquivos e inspeção direta, sem alegar diff Git confiável.
- O banco TESTE oficial é `gestor_pecas_test`; o REAL é `gestor_pecas`. A separação TESTE/REAL deve ser confirmada por `current_database()` antes de qualquer ação destrutiva ou DDL.
- Integrações TOTVS devem permanecer desligadas durante promoção estrutural; schema atualizado não significa outbound habilitado.

References:

- Runbook: `docs/PROMOCAO_SCHEMA_REAL_11_19.md`.
- Estado final confirmado: TESTE `gestor_pecas_test`, schema 24; REAL `gestor_pecas`, schema 11; migration 25 criada mas não aplicada; backup REAL não iniciado; promoção REAL não iniciada.
- Mensagem final do agente: “Nenhuma nova ação será executada. O banco REAL permanece intacto no schema 11.”
