thread_id: 01a068bb-a9ae-7f61-9123-608f25aee3b2
updated_at: 2026-09-04T12:23:16+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\09\03\rollout-2026-09-03T16-25-24-01a068bb-a9ae-7f61-9123-608f25aee3b2.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 1 de correções e estabilização do Gestor de Peças foi concluída com validação automatizada verde

Rollout context: Trabalho realizado no checkout de teste `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, usando exclusivamente o banco `gestor_pecas_test`. O usuário exigiu continuidade exata do ponto anterior, sem refazer alterações corretas, sem iniciar a Wave 2, sem alterar o banco real e sem transformar dados incompletos do PCP/TOTVS em regras de negócio.

## Task 1: Corrigir e validar a Wave 1 completa

Outcome: success

Preference signals:

- Ao retomar o trabalho, o usuário pediu: "Continue exatamente de onde parou na Wave 1. Não recomece nem refaça alterações já aplicadas." Isso indica que futuras continuações devem começar por inspecionar o estado atual e as falhas pendentes, evitando reauditoria ou refatoração desnecessária.
- O usuário reforçou: "Não iniciar Wave 2" e "Use o código atual como fonte de verdade." Em tarefas semelhantes, limitar o trabalho ao escopo solicitado e não antecipar etapas posteriores.
- O usuário exigiu separar bug do Gestor de dado incompleto de PCP/TOTVS e preservar integrações canônicas. Correções devem reutilizar `OperatorFlowService`, outbox, contratos existentes e leitura oficial do SigmaNEST, sem mocks, fuzzy matching ou serviços paralelos.

Key steps:

- A auditoria encontrou que a leitura do roteiro completo misturava pertencimento à OP com elegibilidade do posto: a operação atual era escolhida incorretamente a partir do setor da tela. O serviço passou a retornar o roteiro inteiro com estados `done`, `current` e `pending`, mantendo operações não apontáveis visíveis e calculando `pointable`, `sector_compatible`, `resource_compatible` e `actionable`.
- O roteiro completo passou a incluir operações de inspeção e marcos do snapshot TOTVS como contexto, sem torná-los apontáveis pelo posto produtivo.
- A conclusão de Corte passou a considerar a evidência canônica de tarefa Destaque finalizada e todos os nestings ativos finalizados, em vez de exigir um `apontamento_operacionais` fictício para Corte.
- A fila local da Qualidade recebeu a mesma regra para reconhecer a conclusão canônica de Corte.
- O endpoint local de consulta de OP deixou de construir o provisioning corporativo quando a OP já existe; provisioning só participa no caminho de MISS.
- O teste de sequência foi ajustado para percorrer o fluxo canônico Destaque → Corte → Dobra → Inspeção → Pintura, incluindo abertura e conclusão da inspeção pela `QualityInspectionService`.
- Documentação de `ROADMAP.md`, `README.md` e `AGENTS.md` foi atualizada para registrar a Wave 1, schema 22, regras de `mm`, retrabalho rastreável e conclusão canônica de Corte.

Failures and how to do differently:

- A primeira suíte completa encontrou 1 erro e 1 falha: o dublê `ApiFakeDatabase` não suportava a construção eager do provisioning remoto, e a sequência de Pintura falhava porque o Corte é concluído por tarefa/nesting, não por apontamento operacional. A correção foi tornar o provisioning lazy e integrar a evidência canônica do Corte ao roteiro e à fila de Qualidade.
- Uma tentativa de patch falhou por contexto incorreto; a edição seguinte foi aplicada com contexto mais específico. Em futuras alterações, verificar o trecho atual antes de aplicar patches.
- O teste de Pintura inicialmente usou a chave inexistente `produto_codigo` no retorno público da inspeção; o contrato correto expõe `produto`. O teste foi ajustado sem alterar o contrato do serviço.
- O checkout não possui metadados Git (`NO_GIT_METADATA`), portanto não foi possível produzir um `git diff` confiável. O conjunto alterado foi controlado por inventário de arquivos e inspeção direta.
- O log de migration com `CheckViolation` foi proveniente de teste negativo que injeta violação deliberadamente; não foi falha final. A suíte completa terminou com `OK`.

Reusable knowledge:

- O banco efetivamente usado foi confirmado via `conninfo_to_dict(cfg.dsn)`: `DATABASE=gestor_pecas_test`. A versão aplicada foi confirmada diretamente em `schema_migrations`: `APPLIED_SCHEMA=22`.
- A conclusão de Corte não deve ser inferida apenas de `apontamentos_operacionais`; deve verificar tarefa Destaque finalizada, existência de planos SigmaNEST ativos e ausência de nesting ativo não finalizado.
- A fila da Qualidade é local e só deve liberar uma OP quando existe a operação `INSPECAO`, as operações produtivas anteriores estão concluídas e a inspeção não está finalizada. Ela não deve consultar GPOPSYNC/TOTVS.
- A operação `INSPECAO` é persistida como metadado do roteiro (`inspecao_qualidade = TRUE`, `ativo = FALSE`, `tipo_setor = NULL`) e é executada pela aba Qualidade via `OperatorFlowService`, não por um fluxo paralelo.
- O retorno de retrabalho deve preservar OP, peça/item, inspeção originadora e operação produtiva anterior aplicável, sem criar produção nova ou outbound paralelo.
- O build frontend terminou com aviso conhecido de chunk acima de 500 kB, mas sem erro de compilação.

References:

- Backend completo: `C:\Python314\python.exe -m unittest discover -s tests` → `Ran 620 tests ... OK (skipped=1)`.
- Suíte direcionada final: `C:\Python314\python.exe -m unittest tests.test_operator_flow tests.test_cut_service tests.test_quality_inspection tests.test_totvs_operator_queue tests.test_web_api.WebApiTests.test_fluxo_web_operador_reutiliza_servico_transacional_e_csrf` → `Ran 94 tests ... OK`.
- Frontend: `npm test -- --run` em `web` → `7 passed`, `63 passed`.
- Build/typecheck: `npm run build` em `web` → `tsc -b && vite build`, `382 modules transformed`, exit 0.
- Compilação: `C:\Python314\python.exe -m compileall -q app backend mes tests` → `COMPILEALL_OK`.
- Varredura de corrupção textual/debug: `UNICODE_SCAN_OK`; nenhum `TODO`, `FIXME`, `console.log` ou `debugger` relevante nos arquivos afetados.
- Arquivos centrais: `app/database/database.py`, `app/database/quality_repository.py`, `app/database/migrations.py`, `mes/services/operator_flow.py`, `mes/services/cut.py`, `mes/services/quality.py`, `backend/api/routers/operator.py`, `web/src/pages/operator/WorkbenchPage.tsx`, `web/src/pages/operator/QualityInspectionPage.tsx`, `web/src/pages/operator/CuttingPage.tsx`, `web/src/pages/AIPage.tsx`, `web/src/pages/AndonPage.tsx`, `web/src/pages/home/HomePages.tsx`, `web/src/styles/global.css`, `ROADMAP.md`, `README.md`, `AGENTS.md`.
- Pendências explicitadas: não houve nova movimentação produtiva real no TOTVS; não houve nova inspeção visual manual autenticada em todas as resoluções; dados incompletos de PCP/SigmaNEST continuam dependentes de validação externa.
