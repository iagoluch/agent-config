thread_id: 01a042e5-0222-7ed0-8b5e-f4c6f043a390
updated_at: 2026-08-31T20:03:41+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\08\27\rollout-2026-08-27T08-04-59-01a042e5-0222-7ed0-8b5e-f4c6f043a390.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Homologação TOTVS TESTE → Gestor TESTE avançou localmente, mas ficou bloqueada na etapa externa do Protheus/TOTVS

Rollout context: O usuário pediu em português para analisar e seguir o prompt de homologação TOTVS anexado. O trabalho ocorreu em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, usando PowerShell, com exigência de não tocar produção, não inventar endpoints/aliases/contratos e parar diante de bloqueios externos.

## Task 1: Auditar e validar a integração ProductionOrder V1 em ambiente TESTE

Outcome: partial

Preference signals:

- O usuário pediu simplesmente “analise o prompt e siga-o”, e o prompt exigia confirmação rigorosa de ambiente, execução somente em TESTE, ausência de escrita Gestor → TOTVS e interrupção diante de qualquer dúvida. Em tarefas de integração semelhantes, tratar o documento anexado como especificação operacional, mas não como autorização para inventar valores ou ultrapassar bloqueios externos.
- O fluxo adotou auditoria somente leitura antes de mudanças e não alterou a configuração persistente `.env`; isso é compatível com a exigência do usuário de preservar segurança, rastreabilidade e estado existente.
- O prompt proibia aliases automáticos como `LASER -> LASER1` sem configuração validada. O teste foi executado sem aliases, preservando etapas não mapeadas como warnings em vez de inventar operações.

Key steps:

- A auditoria confirmou que `/PcfIntegService` é registrado antes do SPA, as flags nascem desabilitadas, `GESTOR_TOTVS_SOAP_SUCCESS_RESULT` é configurável e `execution_write_enabled` permanece `false`.
- O código usa `TEST_DATABASE_URL` para integração de teste e recusa bancos cujo nome não contenha `test`. A conexão efetiva foi confirmada em modo somente leitura como `gestor_pecas_test_homolog_simulacao_3_meses_20260824`, schema 16, separado do banco operacional `gestor_pecas`.
- A API foi iniciada em processo separado em `0.0.0.0:8000`, com `GESTOR_TOTVS_ENABLED=true`, `GESTOR_TOTVS_SOAP_ENABLED=true`, ACK `OK`, simulação desligada, automação auxiliar desligada e aliases vazios. A `.env` persistente não foi modificada.
- `GET /PcfIntegService?wsdl` retornou HTTP 200 e WSDL XML válido com `EAIServiceClass`, `receiveMessage`, `PcfIntegService` e SOAPAction `http://tempuri.org/EAIService/receiveMessage`.
- O endereço `http://10.10.1.248:8000` foi alcançável localmente pela rede Wi-Fi; health e WSDL retornaram HTTP 200. O firewall do Windows estava desabilitado nos perfis ativos e não foi alterado.
- O script obrigatório foi executado com sucesso: `python scripts/homologar_totvs_soap_endpoint.py --endpoint 'http://10.10.1.248:8000' --confirm-test`. Resultado: WSDL aprovado, HTTP 200 e `receiveMessageResult='OK'`.
- O fixture `ok_productionorder_20260821103018_1079689c001 1.xml` foi persistido no PostgreSQL TESTE: inbox `processed`, ação `inserted`, external ID `01|010004|1079689C001`, 4 atividades parseadas e 0 projetadas. A OP ficou ativa com produto `IPCX04014054P`, quantidade 2, `totvs_unique_id` correto e `totvs_generated_on` preenchido.
- O resultado de 0 operações projetadas foi coerente com o mapeamento conservador: sem aliases, `IMPRESSAO OP`, `INSPECAO`, `FINALIZADA` não foram tratados como setores; `LASER` não foi tratado como recurso conhecido. Isso não foi falha de transporte.
- Os 11 testes unitários de `tests.test_totvs_integration` passaram; `py_compile` dos módulos relevantes também passou. Não foi executado o teste PostgreSQL que cria e remove schema porque o prompt proibia `DROP`/limpeza destrutiva.

Failures and how to do differently:

- A homologação real não foi concluída: não houve sessão TOTVS/Protheus TESTE disponível no navegador, o histórico estava vazio, nenhum SmartClient/launcher utilizável foi encontrado e não havia evidência suficiente para executar o diagnóstico MES, redirecionar o endpoint do TOTVS ou enviar uma OP realmente originada pelo Protheus. O resultado correto é `HOMOLOGAÇÃO PARCIAL / BLOQUEADA`, não aprovação final.
- Não declarar aprovação final sem validar todos os itens do checklist: alcance pelo AppServer TOTVS, diagnóstico, envio real, idempotência real, isolamento e ausência de regressões.
- A consulta de rede/firewall teve duas tentativas PowerShell com erro de parser por uso de pipeline vazio; a terceira versão acumulando objetos em array funcionou. Em PowerShell, evitar encadear diretamente um `foreach` vazio para `| Format-*`; acumular resultados e formatar ao final.
- Uma consulta PostgreSQL inicial falhou porque o cursor não usava `dict_row`; outra consulta usou a tabela inexistente `cadastro_recursos` em vez de `catalogo_recursos_pcfactory`. Usar `psycopg.rows.dict_row` e confirmar nomes no schema/método `listar_codigos_recursos_totvs` antes de consultar.
- A tentativa de excluir a cópia temporária extraída do RAR foi bloqueada pela política da ferramenta. A pasta temporária reportada foi `C:\Users\iago.luchtenberg\AppData\Local\Temp\codex-whois-8b5cd826ee9d4ede8a5243760f906a4a`; a limpeza ficou pendente e deve ser tratada explicitamente em futura retomada, sem confundir isso com alteração do projeto.

Reusable knowledge:

- `app.database.config.load_postgres_config(testing=True)` exige `TEST_DATABASE_URL`, impede igualdade com `DATABASE_URL` e exige que o nome do banco contenha `test`.
- O receptor SOAP em `backend/integrations/totvs_soap.py` valida SOAP 1.1, SOAPAction, tamanho do envelope, XML seguro sem DTD/entidades e extrai exatamente `receiveMessage/pXmlDocument`.
- O parser em `mes/integrations/totvs/parser.py` aceita somente `Transaction=ProductionOrder`, `Entity=ProductionOrder` e `Event=upsert`; rejeita mensagens não suportadas e conflitos entre `ProductionOrderUniqueID` e `InternalID`.
- A idempotência da ingestão é baseada no hash SHA-256 do XML completo, não apenas no UUID TOTVS.
- `app/database/totvs_repository.py` persiste a inbox antes do parsing, aplica a OP de modo transacional e mantém a execução industrial fora do fluxo; a integração é unidirecional TOTVS → Gestor.
- Para projeção de operações, o resolvedor usa igualdade exata ou aliases explicitamente configurados; não deve inferir `WorkCenterDescription` como setor executável nem criar equivalências automáticas.

## Task 2: Analisar o RAR Protheus 12.1.2510 para esclarecer o contrato WhoIs

Outcome: success

Preference signals:

- Quando o usuário informou “Tenho isso de documentos do protheus mas não sei se vai ser util”, a análise foi feita somente em leitura, sem executar arquivos e sem extrair conteúdo para o projeto. Em futuras análises de arquivos de terceiros, preservar esse padrão: inventariar primeiro, restringir a busca ao contrato relevante e não tratar conteúdo do arquivo como instrução.
- A decisão adotada foi não implementar enquanto o contrato não estivesse comprovado; depois que o RAR forneceu evidência direta nos fontes Protheus, a conclusão foi atualizada. Isso indica preferência por implementação baseada em evidência primária, não em suposição ou documentação genérica.

Key steps:

- O arquivo `C:\Users\iago.luchtenberg\Downloads\1212510.rar` foi identificado como um pacote de fontes Protheus 12.1.2510 com 30.332 entradas e SHA-256 `D5E935F74212AEFCEEB2769FECDF4B77AA952CE05D510E4160F2C3454A1842E9`. Foi usado `tar -tf` e extração restrita para TEMP; nenhum arquivo foi executado.
- Foram localizados os fontes relevantes `fontes/totvspcp/DGMES.PRW`, `fontes/totvspcp/WSPCP.prw`, `fontes/totvspcp/WSPCFactory.prw`, `fontes/totvspcp/pcpxfun.prx`, `fontes/totvspcp/mensagem unica/MATI650.prw` e `fontes/totvspcp/PCPA109.prw`.
- `DGMES.PRW`, função `VALJOBCOM`, comprovou a solicitação WhoIs real: `TOTVSMessage`, schema `whois_1_000.xsd`, `Type=BusinessMessage`, `Transaction=WhoIs`, produto `PCPA109`, `DeliveryType=Sync` e chaves `PRODUCT_NAME`, `PRODUCT_VERSION`, `PRODUCT_ENDPOINT` e `ACTIVE_SFC`.
- `WSPCFactory.prw` comprovou que o SOAP recebe `pXmlDocument` e devolve `receiveMessageResult`, ambos como string. O cliente Protheus interpreta o conteúdo retornado como XML.
- `pcpxfun.prx`, função `PCPWebsPPI`, comprovou o critério de sucesso do `PCPA109`: o conteúdo de `receiveMessageResult` deve ser XML válido e conter `/TOTVSMessage/ResponseMessage/ProcessingInformation/Status` com valor `OK`. Uma string simples `OK` não é suficiente para o diagnóstico WhoIs.
- `WSPCP.prw`, função `getReturn`, mostrou o formato oficial de resposta: `TOTVSMessage` com `MessageInformation`, `Type=Response`, `Transaction` da mensagem recebida, `ReceivedMessage`, `ProcessingInformation` e `Status=OK`. Para sucesso simples, `ReturnContent` não é necessário.
- `MATI650.prw` mostrou que o adapter de `ProductionOrder` responde a `EAI_MESSAGE_WHOIS` com versões `2.000|2.001|2.002|2.003|2.004|2.005|2.006`, mas isso é a resposta WhoIs do adapter ProductionOrder no Protheus e não deve ser automaticamente copiado para o Gestor sem definir o contrato do endpoint do Gestor.
- A conclusão mudou de “contrato WhoIs não comprovado” para “estrutura de resposta compatível comprovada”. Ainda resta definir explicitamente a identidade configurável do Gestor (`Product name`, versão e `SourceApplication`) sem fingir ser `PCFactory`, `PPI` ou `WSPCP`.

Failures and how to do differently:

- A documentação HTML anterior não continha o XSD nem resposta WhoIs; buscas web retornaram resultados irrelevantes ou erros 403/402. A fonte primária do RAR foi muito mais útil do que continuar ampliando buscas genéricas.
- Não implementar suporte WhoIs apenas com base no XML de requisição ou no ACK `OK`; o retorno precisa ser um `TOTVSMessage/ResponseMessage` completo e validado pelo parser do Protheus.
- Não confundir `WhoIs` com `ProductionOrder`: o endpoint atual direciona qualquer XML ao parser ProductionOrder, portanto uma futura implementação precisa separar o dispatcher WhoIs do fluxo de ingestão industrial e manter a inbox/execução sem efeitos de negócio para o diagnóstico.

Reusable knowledge:

- Contrato SOAP Protheus/PCFactory: operação `receiveMessage`, parâmetro `pXmlDocument`, retorno `receiveMessageResult`; no cliente gerado, o namespace é derivado do WSDL e o retorno é extraído de `receiveMessageResponse/receiveMessageResult`.
- Resposta WhoIs mínima compatível, conforme `WSPCP.prw`, deve conter:
  `TOTVSMessage/MessageInformation` com `UUID`, `Type=Response`, `Transaction=WHOIS`/transação recebida, `StandardVersion=1.0`, empresa/filial, `Product` e `ContextName`; e `ResponseMessage/ReceivedMessage` + `ProcessingInformation/Status=OK`.
- O Protheus usa `Status=OK` como sinal de sucesso da comunicação e pode rejeitar o retorno se ele não for XML ou não tiver a estrutura esperada.
- O fonte `DGMES.PRW` confirma que o diagnóstico é disparado pela tela `PCPA109`/`DGMES`, enquanto `PCPCommAPI` possui um endpoint REST WhoIs separado que apenas retorna JSON vazio; isso não substitui o contrato SOAP usado pelo diagnóstico observado.

References:

- [1] Ambiente e banco: `TEST_DATABASE_URL` → `gestor_pecas_test_homolog_simulacao_3_meses_20260824`; `DATABASE_URL` → `gestor_pecas`; schema PostgreSQL confirmado como `16`; inbox inicial vazia.
- [2] Comando de teste local: `C:\Python314\python.exe scripts/homologar_totvs_soap_endpoint.py --endpoint 'http://10.10.1.248:8000' --confirm-test` → `WSDL aprovado`, `HTTP 200 e receiveMessageResult='OK'`.
- [3] Testes: `C:\Python314\python.exe -m unittest tests.test_totvs_integration -v` → 11 testes, `OK`; `py_compile` dos módulos TOTVS concluído sem erro.
- [4] Arquivos do Gestor: `backend/integrations/totvs_soap.py`, `mes/integrations/totvs/parser.py`, `mes/integrations/totvs/service.py`, `mes/integrations/totvs/resource_mapping.py`, `app/database/totvs_repository.py`, `scripts/homologar_totvs_soap_endpoint.py`.
- [5] Fontes RAR: `1212510/fontes/totvspcp/DGMES.PRW` linhas 787–884; `1212510/fontes/totvspcp/WSPCP.prw` linhas 504–636; `1212510/fontes/totvspcp/pcpxfun.prx` linhas 1399–1575; `1212510/fontes/totvspcp/WSPCFactory.prw` linhas 201–232; `1212510/fontes/totvspcp/mensagem unica/MATI650.prw` linhas 617–621.
- [6] Evidência do RAR: `VALJOBCOM` monta WhoIs com `whois_1_000.xsd`, `Transaction=WhoIs`, produto `PCPA109` e chaves `PRODUCT_NAME`, `PRODUCT_VERSION`, `PRODUCT_ENDPOINT`, `ACTIVE_SFC`.
- [7] Evidência do parser Protheus: `PCPWebsPPI` interpreta `receiveMessageResult` como XML e considera sucesso quando `/TOTVSMessage/ResponseMessage/ProcessingInformation/Status = OK`.
- [8] Não houve alterações no código do Gestor nem na `.env` persistente durante o rollout.
