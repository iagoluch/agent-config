thread_id: 01a03f4a-f221-7223-b0c6-5544cde36af5
updated_at: 2026-08-26T19:06:07+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\08\26\rollout-2026-08-26T15-17-51-01a03f4a-f221-7223-b0c6-5544cde36af5.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# TOTVS ProductionOrder V1 foi implementada e o banco oficial de teste foi consolidado

Rollout context: No checkout `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, o usuário pediu primeiro a execução integral de uma especificação de integração TOTVS/Protheus e depois a identificação/consolidação do banco usado pela porta 8001, com exclusão dos demais bancos de teste e preservação do banco real.

## Task 1: Implementar integração TOTVS ProductionOrder V1

Outcome: success

Preference signals:

- O usuário solicitou que o prompt fosse efetivamente executado, não apenas analisado. A implementação respeitou o escopo `TOTVS → Gestor`, sem escrita de volta ao TOTVS e sem criar um domínio paralelo de OPs.
- A especificação exigia preservar códigos como strings, evitar fuzzy matching, manter `data_emissao` nula quando semântica não fosse comprovada, usar persistência incremental por OP e tratar etapas não suportadas como warnings. Isso indica que futuras integrações devem priorizar preservação semântica e comportamento conservador em vez de preencher lacunas por inferência.

Key steps:

- Auditado o baseline: schema inicial 15, `publicar_catalogo_pcp` confirmado como snapshot global e inadequado para uma única mensagem incremental, `catalogo_pcp_ops`/`catalogo_operacoes_op` confirmados como catálogos canônicos, XMLs reais e referências SOAP disponíveis no workspace.
- Criados DTOs tipados, parser seguro com `defusedxml`, mapper conservador, resolver explícito de setor/recurso, serviço de ingestão, repository PostgreSQL, migration 16, inbox/auditoria, importador local e adapter SOAP 1.1.
- O contrato SOAP implementado ficou fora de `/api/v1`: `GET /PcfIntegService?wsdl` e `POST /PcfIntegService`, com `SOAPAction=http://tempuri.org/EAIService/receiveMessage`.
- Copiados byte a byte os dois XMLs reais para `tests/fixtures/totvs/` e os três arquivos SOAP/XSD para `docs/fixtures/totvs/`; hashes SHA-256 confirmaram cópias idênticas.
- Corrigida uma incompatibilidade descoberta na homologação: `catalogo_recursos_pcfactory` usa a coluna `habilitado`, não `ativo`.
- Corrigido teste legado de migration para lidar com a presença da migration 16 e validar reaplicação de uma lacuna sem confundir `MAX(version)` com o conjunto aplicado.

Reusable knowledge:

- A migration 16 adiciona inbox `totvs_integration_messages`, metadados TOTVS em `catalogo_pcp_ops`, identidade de atividade em `catalogo_operacoes_op`, índices de unicidade corporativa e torna `catalogo_pcp_ops.data_emissao` nullable. Não usar `GeneratedOn` ou `StartOrderDateTime` como data de emissão.
- Idempotência tem dois níveis: hash SHA-256 do payload para deduplicar a mesma mensagem e `ProductionOrderUniqueID` para atualizar a mesma OP sem duplicá-la. O UUID não pode ser chave exclusiva porque os dois fixtures usam `UUID=1`.
- O processamento é transacional e local à OP; não chamar `Database.publicar_catalogo_pcp([uma_op])`, pois esse método inativa registros ausentes do snapshot global.
- Parser e adapter recusam DTD/ENTITY/XXE, XML malformado, payload acima do limite, SOAPAction/operação incorretos e `pXmlDocument` ausente. O payload integral não é emitido em logs ou SOAP Faults.
- O mapper preserva todas as atividades no DTO, mas somente projeta setor/recurso quando há correspondência exata ou alias explícito. `LASER` não vira `LASER1` sem configuração.
- O default é fechado: `GESTOR_TOTVS_ENABLED=false`, `GESTOR_TOTVS_SOAP_ENABLED=false`; habilitar SOAP exige `GESTOR_TOTVS_SOAP_SUCCESS_RESULT` confirmado externamente. `execution_write_enabled` permanece sempre false.
- Homologação real no banco de teste confirmou OP `10796502001` com 9 atividades parseadas/3 projetadas e OP `1079689C001` com 4 parseadas/1 projetada; a OP alfanumérica permaneceu string. Ambas ficaram ativas e a reentrega retornou `action=duplicate`/`idempotent=true`.

Failures and how to do differently:

- O primeiro importador falhou porque a consulta procurava `ativo` em `catalogo_recursos_pcfactory`; verificar o schema efetivo das tabelas antes de reutilizar nomes de colunas.
- A primeira regressão ampla teve 1 falha em teste antigo que esperava schema 14 após remover a migration 15, embora a migration 16 já estivesse presente. Ajustar testes de migrations para validar lacunas/reaplicação com versões posteriores, não apenas `MAX(version)`.
- O checkout não tinha metadados Git utilizáveis; inventários devem ser feitos por inspeção direta de arquivos e comandos.

References:

- `mes/integrations/totvs/{models.py,parser.py,mapper.py,resource_mapping.py,service.py,errors.py}`
- `app/database/totvs_repository.py`, `app/database/migrations.py`, `app/database/schema.py`
- `backend/integrations/totvs_soap.py`, `backend/api/config.py`, `backend/api/main.py`
- `scripts/import_totvs_production_order.py`
- `tests/test_totvs_integration.py`, `tests/test_totvs_postgres.py`
- Regressão final: `C:\Python314\python.exe -m unittest discover -s tests -p "test_*.py"` → `Ran 307 tests`, `OK`.
- Banco usado na homologação TOTVS: `gestor_pecas_test_simulacao_residencia_20260824`; depois o usuário pediu sua exclusão durante a consolidação dos bancos.

## Task 2: Identificar a base da porta 8001 e consolidar bancos de teste

Outcome: partial

Preference signals:

- O usuário pediu: “veja qual banco teste está sendo usado na porta 8001 e deixe ele como banco teste oficial, exclua os outros testes e mantenha o banco real ainda” — futuras ações destrutivas devem primeiro identificar o processo/listener, comparar nomes e contagens, proteger explicitamente o banco real e somente então excluir alvos exatos.
- A confirmação esperada inclui a porta, processo, banco efetivo, schema/status, banco real preservado e lista explícita dos bancos removidos.

Key steps:

- Identificado o listener `127.0.0.1:8001`, PID 20620, executando `C:\Python314\python.exe tests\simulacao_historica_3_meses\run_web_simulacao.py`.
- O processo da porta 8001 usava `gestor_pecas_test_homolog_simulacao_3_meses_20260824`, não o banco originalmente presente no `.env`.
- Comparados bancos de teste por contagens; o banco da porta 8001 continha 1.752 OPs/apontamentos, 29.391 eventos de estado, 5.040 eventos de quantidade, 12 sessões e 24 rateios.
- Preservados `gestor_pecas` como banco real, `postgres` como banco de manutenção e `gestor_pecas_test_homolog_simulacao_3_meses_20260824` como banco oficial.
- Excluídos com `DROP DATABASE ... WITH (FORCE)`: `gestor_pecas_seed_test`, `gestor_pecas_test`, `gestor_pecas_test_homologacao_extrema_20260820`, `gestor_pecas_test_residencia_20260824` e `gestor_pecas_test_simulacao_residencia_20260824`.
- Atualizados `.env.example`, `.env` e `scripts/run_simulacao_residencia.py` para apontar ao banco oficial; a migration 16 foi aplicada ao banco oficial.
- Validação final confirmou no banco oficial schema 16, dados preservados e `totvs_integration_messages=0`; `gestor_pecas` continuou conectável.

Reusable knowledge:

- Configuração final do teste: `TEST_DATABASE_URL` aponta para `gestor_pecas_test_homolog_simulacao_3_meses_20260824` em `127.0.0.1:15432`; `POSTGRES_DB` no `.env.example` também foi alinhado a esse nome.
- A porta 8001 respondeu `status=ok`, PostgreSQL `available`, schema 16, `active_data_source=postgresql_test_only`, simulação habilitada e referência `2026-08-24 08:32:00`.
- O banco real `gestor_pecas` foi preservado e sua conectividade foi confirmada. Bancos de sistema não foram removidos.
- O processo antigo da porta 8000 não pôde ser encerrado por `Stop-Process` devido a “Acesso negado”. Mesmo assim, o banco associado foi removido com `DROP DATABASE ... WITH (FORCE)`, e a porta 8000 passou a responder HTTP 503. Para limpeza completa do ambiente, ainda é necessário encerrar esse processo em PowerShell elevado e reiniciá-lo com a nova configuração.

Failures and how to do differently:

- A tentativa de encerrar o PID 19524 da porta 8000 falhou por permissão. Não insistir com a mesma sessão; usar terminal elevado ou encerrar pelo usuário/serviço proprietário.
- Uma auditoria de listeners falhou por sintaxe PowerShell ao usar pipe vazio; preferir acumular resultados em array antes de formatar.
- Uma consulta de validação falhou por concatenação de string/dicionário (`TypeError`); converter explicitamente objetos estruturados para string/JSON.
- O banco oficial foi identificado por evidência do processo e contagens, não apenas pelo `.env`; manter esse procedimento para evitar excluir o banco errado.

References:

- Listener: `127.0.0.1:8001`, PID `20620`, comando `tests\simulacao_historica_3_meses\run_web_simulacao.py`.
- Banco oficial: `gestor_pecas_test_homolog_simulacao_3_meses_20260824`.
- Banco real preservado: `gestor_pecas`.
- Porta 8001 após consolidação: health `ok`, database `available`, schema `16`.
- Porta 8000: processo PID `19524` permaneceu ativo por falta de permissão e retornou HTTP `503` após a exclusão de seu banco anterior.
- Arquivos alinhados: `.env`, `.env.example`, `scripts/run_simulacao_residencia.py`.

