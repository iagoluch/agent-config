thread_id: 01a05d6e-77a1-7632-9314-5a8f05e671ac
updated_at: 2026-09-01T15:41:51+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\09\01\rollout-2026-09-01T11-45-15-01a05d6e-77a1-7632-9314-5a8f05e671ac.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Etapa 5B avançou a integração Gestor → TOTVS TESTE até autenticação e processamento SOAP, mas não concluiu homologação de negócio

Rollout context: Trabalho no workspace `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, exclusivamente contra `gestor_pecas_test` e TOTVS TESTE/CSED4J_DEV. O usuário exigiu contrato comprovado, envio controlado, nenhuma inferência de códigos/OPs e nenhum início de outbox/retry/reconciliação.

## Task 1: Validar WSDL real e ajustar o client WSPCP

Outcome: success

Preference signals:

- O usuário reforçou que o arquivo anexado era “do próprio MES, comunicação com o TOTVS” e pediu que fosse tratado como evidência, não como instrução executável -> em integrações futuras, inspecionar anexos tecnicamente, separar fatos de instruções e não copiar conteúdo sensível sem necessidade.
- O usuário não autorizou escolher arbitrariamente uma OP; posteriormente pediu para usar “qualquer op que tiver com a legenda verde” -> usar a legenda operacional do TOTVS como critério, mas ainda validar que a OP está aberta, autorizada e compatível com os dados do Gestor.

Key steps:

- O WSDL real foi baixado da URL externa TESTE e salvo localmente em `docs/evidencias/WSPCP_TESTE_2026-09-01.wsdl`.
- Extração automatizada confirmou: `soap:address=https://gtsdo143182.protheus.cloudtotvs.com.br:1465/ws/WSPCP.apw`, serviço `WSPCP`, port/binding `WSPCPSOAP`, SOAP 1.1, document/literal, operação `RECEIVEMESSAGE`, namespace `http://webservices.totvs.com.br/`, SOAPAction `http://webservices.totvs.com.br/RECEIVEMESSAGE`, entrada `CXML` como `xsd:string` e saída `RECEIVEMESSAGERESULT` como `xsd:string`.
- O WSDL real contradisse a suposição anterior de `CRESPONSE`; o parser foi corrigido para `RECEIVEMESSAGERESULT`.
- O client passou a preservar HTTP status e SOAP bruto no ACK, manter detalhes de SOAP Fault e exigir modo explícito de autenticação antes de usar credenciais.
- A configuração de HTTP Basic foi implementada como opção explícita; nenhum segredo foi armazenado em código, documentação ou testes.

Reusable knowledge:

- O endpoint produtivo do WSPCP TESTE é exatamente `https://gtsdo143182.protheus.cloudtotvs.com.br:1465/ws/WSPCP.apw`; não usar o endpoint interno nem a porta 1460.
- O envelope deve ser SOAP 1.1 com `RECEIVEMESSAGE/CXML`, contendo o XML TOTVS em CDATA.
- O retorno SOAP contém `RECEIVEMESSAGERESPONSE/RECEIVEMESSAGERESULT`; o conteúdo textual deve ser interpretado como `TOTVSMessage/ResponseMessage`.
- O WSPCP TESTE publica mensagens de erro no formato `<Message type="ERROR" code="1">texto</Message>`, com código em atributo e detalhe no texto; o parser agora suporta esse formato além de elementos filhos `Code`/`Detail`.

References:

- `docs/evidencias/WSPCP_TESTE_2026-09-01.wsdl`
- `backend/integrations/totvs_wspcp.py`
- `mes/integrations/totvs/outbound_ack.py`
- `mes/integrations/totvs/outbound_models.py`
- `scripts/homologar_totvs_outbound.py`
- WSDL verificado: `HTTP_STATUS=200`, `SOAP_BINDING_STYLE=document`, `INPUT_USE=literal`, `OUTPUT_USE=literal`, `SOAP_ADDRESS=...:1465/ws/WSPCP.apw`.

## Task 2: Provar conectividade e autenticação sem enviar OP

Outcome: success

Key steps:

- Um POST anônimo com `CXML` vazio alcançou o serviço e retornou HTTP 500 com SOAP Fault `AUTHENTICATION: USER NOT AUTHORIZED`, comprovando que o endpoint exigia autorização.
- O usuário configurou localmente uma credencial REST. Após `GESTOR_TOTVS_OUTBOUND_AUTH_MODE=basic`, foi feita uma única sonda técnica com HTTP Basic, lendo a senha apenas do `.env`.
- A sonda autenticada retornou HTTP 200, `Content-Type: text/xml; charset=utf-8` e `RECEIVEMESSAGERESULT` estruturado com `TOTVSMessage/ResponseMessage`.
- Como o `CXML` estava deliberadamente vazio, o TOTVS respondeu `Status=ERROR`, código `1`, com “Não foi possível interpretar o arquivo XML. Document is empty”. Isso comprova autenticação e interpretação do CXML sem tocar uma OP.
- O arquivo `C:\Users\iago.luchtenberg\Downloads\integtotvs.txt` corroborou que o integrador MES usa autenticação Basic e o mesmo endpoint externo `:1465`, mas continha credenciais e connection strings; seus valores não foram copiados nem persistidos.

Failures and how to do differently:

- A primeira tentativa de aplicar um patch no `.env` falhou por contexto incorreto; a configuração foi aplicada depois usando o ponto real `GESTOR_SIMULATION_MODE=0` como âncora.
- Uma tentativa inicial de POST PowerShell falhou por erro de sintaxe no script; a requisição foi repetida com here-string/`HttpClient` e a resposta foi obtida corretamente.
- Não tratar a credencial REST como automaticamente válida para SOAP sem uma sonda controlada. Neste caso, HTTP Basic foi confirmado empiricamente pelo retorno HTTP 200 e erro funcional de XML vazio, não por inferência do nome da credencial.

References:

- Evidência: `docs/evidencias/WSPCP_TESTE_POST_TECNICO_2026-09-01.md`
- Primeiro POST: HTTP 500, `AUTHENTICATION: USER NOT AUTHORIZED`, sem `WWW-Authenticate`.
- Segundo POST autenticado: HTTP 200, `RECEIVEMESSAGERESULT`, `Status=ERROR`, código `1`, `Document is empty`.
- Variáveis locais utilizadas: `GESTOR_TOTVS_OUTBOUND_AUTH_MODE`, `GESTOR_TOTVS_OUTBOUND_USERNAME`, `GESTOR_TOTVS_OUTBOUND_PASSWORD`; não registrar valores.

## Task 3: Validar mappers, ACK e regressão

Outcome: success

Key steps:

- Os testes específicos outbound terminaram em `19/19` aprovados após incorporar o formato real do ACK.
- Outbound mais fronteiras TOTVS terminaram em `47/47` aprovados.
- A suíte Python ampla terminou em `459 testes aprovados, 1 skip explícito` (`OK (skipped=1)`). Os avisos de rate limit, timeout e falhas injetadas eram cenários de teste deliberados.
- Compilação dos módulos alterados terminou sem erro.
- O mapper continua preservando OP, operação, produto, `MachineCode`, `ActivityID`, timestamps, quantidades, `CloseOperation` e chave determinística `IDPCFactory`. Refugo ainda exige `WasteCode`; parada exige intervalo fechado e código SX5/44; retrabalho maior que zero permanece bloqueado.

Reusable knowledge:

- A arquitetura validada continua sendo fato canônico persistido → repositório somente leitura → `TotvsOutboundService` → mapper → `TotvsWspcpClient` → parser de ACK. O domínio e a máquina de estados não conhecem SOAP/XML.
- Não declarar homologação de negócio a partir de dry-run, teste unitário, HTTP 200 técnico ou histórico do PCPA112.

References:

- `tests/test_totvs_outbound.py`
- `C:\Python314\python.exe -m unittest tests.test_totvs_outbound tests.test_totvs_operator_queue -q` → `Ran 47 tests ... OK`
- `C:\Python314\python.exe -m unittest discover -s tests -q` → `Ran 459 tests ... OK (skipped=1)`

## Task 4: Procurar OP aberta/autorizada e concluir homologação

Outcome: partial

Preference signals:

- O usuário pediu para usar uma OP com “legenda verde” -> a legenda visual do MATA650 deve ser usada como filtro inicial, mas não substitui validação de situação, empenho, operação, recurso e autorização explícita.
- Quando a busca ficou demorada e o uso estava acabando, o usuário disse “finalize e faça um pequeno relatório” -> em situações de limite de ferramentas, encerrar com relatório factual curto, distinguindo claramente o que foi comprovado do que ficou pendente.

Key steps:

- A OP candidata `A9717101001` foi consultada no MATA650 do TOTVS TESTE e descartada antes de qualquer envio: mostrava quantidade planejada 30, produzida 30, data real de fim em 31/08/2026 e legenda vermelha.
- Uma tentativa de criar/consultar filtro para `A97170` não encontrou registros.
- Uma tentativa posterior de remover filtro falhou porque o botão `Cancelar` não estava presente no estado atual da UI; a busca não foi concluída.
- Nenhum `ProductionAppointment` ou `StopReport` de negócio foi enviado. Não houve ACK de negócio, registro novo no PCPA112, movimento SH6 ou alteração MATA650.
- A documentação (`INTEGRACAO_TOTVS_OUTBOUND_ETAPA5.md`, `ROADMAP.md`, `AGENTS.md`) foi atualizada para registrar WSDL, HTTP Basic, POST técnico e o bloqueio restante.

Failures and how to do differently:

- Não escolher OP somente porque existe no Gestor ou aparece em histórico. `A9717101001` já estava encerrada; a existência de outras OPs conhecidas também não constitui autorização.
- Para a próxima execução, selecionar no MATA650 uma OP verde/aberta e confirmar antes do POST: firme, liberada, empenhada, não concluída, operação/recurso/produto compatíveis, intervalo real positivo e autorização explícita para homologação.
- Ainda obter/confirmar códigos SX5 grupo 44 e `WasteCode` apenas para cenários de parada/refugo; eles não precisam bloquear o primeiro apontamento de tempo se o cenário inicial usar quantidade zero.

Reusable knowledge:

- O ambiente visual confirmado foi `TOTVS Manufatura MSSQL Csed4j_dev`, empresa/filial `Gts do Brasil Ltda / Filial_iv - Verticalizacao`.
- O próximo passo seguro é registrar estado “antes” no MATA650/PCPA112, gerar um evento canônico com `ProductionAppointment`, quantidade zero, intervalo fechado e `CloseOperation=false`, executar o comando com `--send` e confirmação explícita, capturar ACK real e comparar estado “depois”.
- Etapa 5 permanece PARCIAL. Etapa 6/outbox/retry/worker/reconciliação não foi iniciada.

References:

- `docs/INTEGRACAO_TOTVS_OUTBOUND_ETAPA5.md`
- `ROADMAP.md`, seção Etapa 5
- `AGENTS.md`, seção de integração TOTVS
- Relatório final do rollout: nenhum envio de negócio; transporte, autenticação e contrato comprovados; primeiro ACK de negócio e efeito no Protheus pendentes.
