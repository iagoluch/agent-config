thread_id: 01a06781-3ab5-70c2-bbdf-d93a0ccf2622
updated_at: 2026-09-03T14:04:33+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\03\rollout-2026-09-03T10-41-57-01a06781-3ab5-70c2-bbdf-d93a0ccf2622.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Etapa 7B foi concluída com transporte real GPOPSYNC/MATI650 e correção do caso de OP sem roteiro

Rollout context: projeto Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, PowerShell, banco exclusivo `gestor_pecas_test`. O objetivo era fechar a lacuna da Etapa 7A usando o ponto de entrada normal do Gestor e o endpoint real `GESTORPECASPO`, sem repetir a 7A, sem alterar o GPOPSYNC, sem criar parser/pipeline paralelo e sem executar apontamentos ou outbound.

## Task 1: Homologação E2E real da OP principal

Outcome: success

Preference signals:

- O usuário exigiu: “Não refaça a 7A”, “Não criar parser novo”, “Não criar pipeline paralelo” e “Aplicar SOMENTE as regras canônicas já existentes” -> em homologações semelhantes, substituir apenas a fronteira externa e preservar `OrderProvisioningService`, `ProductionOrderOnDemandSyncService`, ingestão canônica, projeções e consulta operacional.
- O usuário pediu para comprovar um MISS local, registrar a chamada real, distinguir efeitos de ingestão de efeitos operacionais e evitar apagar dados produtivos para fabricar MISS -> sempre fazer preflight do banco e demonstrar contagens antes/depois antes de qualquer chamada real.
- O usuário determinou que credenciais fossem usadas por variável de ambiente e nunca aparecessem em código, documentação ou logs -> manter essa política.
- O usuário pediu que a 7A não fosse repetida, pois concorrência, outbox, retry, restart, lease e idempotência já estavam comprovados -> depois de uma chamada real parcialmente validada, reconciliar o estado persistido em vez de repetir o transporte.

Key steps:

- O preflight confirmou `TEST_DATABASE_URL` apontando para `gestor_pecas_test`, mas inicialmente encontrou as variáveis `GESTOR_TOTVS_OP_PULL_*` vazias. A configuração foi adicionada ao `.env` usando o endpoint real e referências às credenciais outbound já existentes, sem copiar valores secretos.
- Antes da chamada, a OP `00615903001` tinha zero registros em `catalogo_pcp_ops`, `catalogo_operacoes_op`, `totvs_integration_messages`, `totvs_op_sync_requests`, `totvs_outbox`, apontamentos e histórico.
- Foi criado `scripts/homologar_totvs_e2e_etapa7b.py`, com gravação de metadados seguros do HTTP real, validações do XML, contagens PostgreSQL, consulta operacional e opção `--inspect-existing-main` para reconciliação sem repetir transporte.
- A chamada real foi `POST https://gtsdo143182.protheus.cloudtotvs.com.br:1467/rest/GESTORPECASPO/gestorpecas/v1/production-order`, corpo `{"companyId":"01","branchId":"010004","number":"00615903001"}`, retornando HTTP 200 e `text/xml; charset=utf-8`.
- O XML real foi processado por `TotvsProductionOrderIngestionService`, gerando inbox `processed/inserted`, cabeçalho canônico e roteiro. A solicitação ficou `DONE`, uma tentativa, com tempo persistido de `1,317123 s`.
- Dados validados: `ProductionOrder`/`message_version=2.004`, `SourceApplication=SIGAPCP`, `MATA650 12.1.2510`, `UniqueID=01|010004|00615903001`, produto `IPCX04014041P`, quantidade 15, `ReportQuantity=0`, `StatusOrderType=1`.
- O roteiro recebido continha `01/IMPRESSAO OP/PCP/PCP`, `10/CORTE/CORTE/LASER`, `20/INSPECAO/CALDER/INSPEC` e `99/FINALIZADA/ALMOX4/ALMOX4`, com `IsActivityEnd=true` na atividade 99.
- As regras canônicas projetaram apenas `10/CORTE` como `LASER1` ativo no setor Corte e preservaram `99/FINALIZADA/ALMOX4` como `marco_terminal=true`, `ativo=false`, `tipo_setor=null`, invisível ao operador. A operação 01 foi tratada como automática/não manual satisfeita e a 20 como qualidade em manutenção.
- A segunda consulta retornou `status=local`, `requested=false`, sem chamada adicional ao ERP. Ingestão não criou outbox, apontamentos, eventos de quantidade, eventos do operador ou histórico.
- Uma primeira execução do verificador falhou depois da chamada e da ingestão porque comparava `2.004` com `standard_version`; o campo correto é `message_version`, enquanto `standard_version` real é `1.0`. O erro foi corrigido e o resultado foi reconciliado sem repetir a chamada principal.

## Task 2: Caso matriz existente no ERP sem roteiro

Outcome: success

Preference signals:

- O usuário instruiu: “Não inventar roteiro” e pediu que a OP matriz fosse tratada conceitualmente como “OP existente no ERP, porém sem roteiro operacional utilizável” -> manter cabeçalho auditável, `found=false`, zero operações e mensagem explícita, sem classificá-la como OP inexistente.

Key steps:

- A OP `01/010001/10795102002` respondeu HTTP 200/XML real, `UniqueID=01|010001|10795102002`, `Quantity=14`, `ReportQuantity=0` e lista de atividades vazia.
- O fluxo originalmente retornava `timeout/indisponível` mesmo após persistir o cabeçalho. Isso foi identificado como bug concreto de representação.
- Foi adicionado o estado `sem_roteiro`, com mensagem `OP existente no TOTVS, porém sem roteiro operacional utilizável.`; o resultado mantém `found=false`, não cria operações nem execução, reconcilia a solicitação para `DONE` e não chama novamente o ERP quando o cabeçalho já existe.
- O banco final preservou o cabeçalho da matriz, zero operações, zero outbox e zero fatos operacionais. As duas chamadas reais totais da etapa foram uma para a OP principal e uma para a matriz; reconciliações posteriores fizeram zero chamadas.

## Task 3: Documentação e regressão

Outcome: success

Key steps:

- Atualizados `ROADMAP.md`, `README.md`, `AGENTS.md`, `protheus/README.md` e `docs/INTEGRACAO_TOTVS_OP_SOB_DEMANDA_ETAPA61.md` para refletir a publicação/homologação real, o encerramento da 7A no escopo controlado e a conclusão da 7B.
- Criada a evidência `docs/evidencias/TOTVS_ETAPA7B_HOMOLOGACAO_REAL_2026-09-03.md`, incluindo endpoint, corpo, tempos, hash do XML, projeções, contagens antes/depois, caso matriz, bugs e pendências.
- Alterados `mes/integrations/totvs/on_demand.py`, `mes/services/order_provisioning.py`, `app/database/totvs_op_sync_repository.py` e `tests/test_totvs_on_demand.py` para suportar a distinção `sem_roteiro`.
- Validação final: compilação Python aprovada; `67` testes Python direcionados aprovados; teste E2E da 7A aprovado; `13` testes Web do operador aprovados; health API OK com schema 20; varredura UTF-8 sem corrupção; banco final `gestor_pecas_test`; outbox global `0`.

Failures and how to do differently:

- O primeiro verificador usou `standard_version` para validar a versão `2.004`. Corrigir verificadores para usar `message_version=2.004`; preservar `standard_version=1.0` como campo distinto.
- O caso sem roteiro foi inicialmente classificado como timeout. O sintoma “HTTP 200 + cabeçalho persistido + zero atividades” deve resultar em estado específico `sem_roteiro`, não em `nao_encontrada` nem `timeout`.
- Após uma chamada real parcialmente validada, não repetir o transporte apenas para completar assertions do instrumento. Consultar inbox, catálogo e tabela de sincronização e corrigir o verificador/reconciliar o estado.
- O processo Web de teste já estava ativo em `8001` e foi preservado; mudanças de `.env` e código só são consumidas no próximo reinício.

Reusable knowledge:

- A fronteira canônica é `OrderProvisioningService → ProductionOrderOnDemandSyncService → ProtheusOnDemandRequestGateway → TotvsProductionOrderIngestionService → catálogo PostgreSQL → consulta/OperatorFlowService`. A camada de execução não deve conhecer o ERP.
- `GESTOR_TOTVS_OP_PULL_MODE=inline` faz o gateway entregar o XML diretamente à ingestão canônica; não deve haver parser, mapper ou persistência paralelos.
- O endpoint real validado é `/rest/GESTORPECASPO/gestorpecas/v1/production-order` na porta 1467, usando Basic Auth por variáveis de ambiente e TLS verificado.
- O terminal `99/FINALIZADA/ALMOX4` deve ser preservado no catálogo uma única vez, inativo, sem setor e invisível ao operador. A ingestão não finaliza a OP e não cria outbound.
- `buscar_op_local_totvs` considera carregável uma OP com cabeçalho e pelo menos uma operação ativa; `buscar_cabecalho_op_local_totvs` permite distinguir cabeçalho existente sem roteiro de MISS verdadeiro.
- O banco de teste é `gestor_pecas_test`; o banco REAL `gestor_pecas` não foi acessado. Não assumir o DSN apenas pela `.env`; confirmar o nome efetivo via `psycopg`.

References:

- `scripts/homologar_totvs_e2e_etapa7b.py` — instrumento reproduzível; `--inspect-existing-main --verify-matrix` reconcilia os casos sem repetir a OP principal.
- `docs/evidencias/TOTVS_ETAPA7B_HOMOLOGACAO_REAL_2026-09-03.md` — evidência final detalhada.
- `ROADMAP.md:1009` — estado oficial da Etapa 7B.
- Endpoint validado: `POST https://gtsdo143182.protheus.cloudtotvs.com.br:1467/rest/GESTORPECASPO/gestorpecas/v1/production-order`.
- Corpo validado: `{"companyId":"01","branchId":"010004","number":"00615903001"}`.
- Hash SHA-256 do XML principal: `ccd1628f7362f4a414e53a90616ceed2e0c7b6a1f5bef6a9339d5687fb630b16`.
- Testes: `.venv\Scripts\python.exe -m dotenv run -- .venv\Scripts\python.exe -m unittest tests.test_totvs_on_demand tests.test_totvs_operator_queue tests.test_totvs_etapa7a_e2e`; resultado final `Ran 67 tests ... OK`.
- Teste Web: `npm test -- --run src/test/operator.test.tsx`; resultado `13 passed`.
