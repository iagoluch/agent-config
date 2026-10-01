thread_id: 01a058fd-8291-75b3-8866-59ec8fa0b5f2
updated_at: 2026-08-31T19:09:15+00:00
rollout_path: \\?\C:\Users\iago.luchtenberg\.codex\sessions\2026\08\31\rollout-2026-08-31T15-03-24-01a058fd-8291-75b3-8866-59ec8fa0b5f2.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Etapa 5 — retorno Gestor → TOTVS implementada, mas homologação ponta a ponta bloqueada

Rollout context: Trabalho no workspace `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, com foco exclusivo nos ambientes `gestor_pecas_test` e TOTVS TESTE. O usuário exigiu implementação real, evidência de contrato, homologação prática e prova antes/depois, sem inventar payloads, códigos, estados ou equivalências.

## Task 1: Descoberta e comprovação do contrato TOTVS outbound

Outcome: partial

Preference signals:

- O usuário pediu explicitamente: “Não inventar qual evento gera cada legenda: provar pelo código e depois pelo TOTVS TESTE” e não considerar a etapa concluída com “apenas XML gerado sem homologação real” -> em tarefas futuras de integração, priorizar evidência de fonte oficial, ACK real e comparação antes/depois; declarar claramente o que permanece não verificado.
- O usuário proibiu inferência de códigos e mapeamentos, especialmente recurso, motivo de parada e refugo -> manter códigos TOTVS como parâmetros explícitos e bloquear envio quando a equivalência não estiver comprovada.
- O usuário determinou que a lógica canônica do operador não fosse alterada nem duplicada -> outbound deve consumir fatos persistidos e nunca criar um fluxo paralelo por origem da OP.

Key steps:

- A documentação oficial capturada do PC-Factory confirmou `ProductionAppointment_2_003` para Protheus e `StopReport_1_001`, além do serviço síncrono `WSPCP.ReceiveMessage` com parâmetro SOAP `CXML` contendo `TOTVSMessage` em CDATA.
- O contrato de produção foi mapeado para `MATA681`/`SH6`: OP (`H6_OP`), operação (`H6_OPERAC`), recurso (`H6_RECURSO`), produto (`H6_PRODUTO`), boas (`H6_QTDPROD`), refugo (`H6_QTDPERD`), início/fim e `CloseOperation` (`H6_PT`).
- O contrato de parada foi mapeado para `MATA682`/`SH6`, exigindo recurso, código de motivo, início, fim e timestamp; retomada fecha a parada anterior, pois não é enviado `StopReport` incompleto.
- O XSD possui `ReworkQuantity`, mas não foi identificado destino efetivo no caminho Protheus/MATA681/SH6; o mapper bloqueia retrabalho maior que zero em vez de convertê-lo silenciosamente.
- A chave de idempotência comprovada é `Identification/key[@name='IDPCFactory']`. O ACK esperado é `TOTVSMessage/ResponseMessage`, com `ProcessingInformation/Status=OK|ERROR`, mensagens e possíveis IDs internos.
- A documentação Protheus/TOTVS confirmou as legendas de OP pelo MATA650: Prevista (`C2_TPOP='P'`); Em aberto sem movimentos e sem ociosidade; Iniciada com movimento SD3/SH6 dentro da janela; Ociosa após `C2_DIASOCI`; Encerrada parcialmente com `C2_DATRF` preenchido e `C2_QUJE < C2_QUANT`; Encerrada totalmente com `C2_DATRF` preenchido e `C2_QUJE >= C2_QUANT`.

Failures and how to do differently:

- Os fontes ADVPL não estavam disponíveis no checkout nem nos diretórios locais pesquisados; não se deve deduzir o contrato apenas pelos nomes `ProductionAppointment`, `StopReport`, `MATI681` ou `MATI682`.
- O WebApp TOTVS TESTE em `https://gtsdo143182.protheus.cloudtotvs.com.br:1460` respondeu HTTP 404 para `/WSPCP.apw?WSDL`. Não testar portas aleatórias: obter da TI a URL/porta real do listener WSPCP, o namespace do WSDL e eventual `SOAPAction`.

Reusable knowledge:

- O PCPA112 do TOTVS TESTE expôs a rotina real “Apontamento de Produção”, com registros “Integrado com sucesso” e “Ocorreram erros”. Foram observados sucessos com quantidade zero e intervalos de início/fim, confirmando suporte a reportes de tempo em condições válidas, mas isso não substitui uma mensagem emitida pelo Gestor.
- OP apenas existente não basta: o PCPA112 mostrou erros históricos como “Ordem de produção sem empenho” e “H6_OP inválido”. A OP de homologação precisa ser firme, liberada, empenhada e autorizada como descartável.

References:

- `docs/INTEGRACAO_TOTVS_OUTBOUND_ETAPA5.md`
- Documentação PC-Factory capturada em `C:\Users\iago.luchtenberg\Documents\Codex\2026-08-27\c\outputs\pcfactory_totvs_mes_html_2026-08-27\`
- Serviço confirmado: `WSPCP.ReceiveMessage`, parâmetro `CXML`
- Rotinas: `ProductionAppointment → MATA681 → SH6`; `StopReport → MATA682 → SH6`; consulta: `PCPA112`

## Task 2: Implementação outbound isolada e protegida

Outcome: success

Preference signals:

- O usuário pediu a separação “evento canônico Gestor → mapper TOTVS → client/gateway” e que o domínio não conhecesse XML SOAP -> preservar essa arquitetura em qualquer extensão futura.
- O usuário pediu envio manual/controlado nesta etapa, sem outbox, retry permanente, worker ou reconciliação contínua -> não antecipar infraestrutura de confiabilidade.

Key steps:

- Criados DTOs neutros, mappers XML, parser de ACK/SOAP Fault, serviço outbound e read model somente leitura.
- O repositório outbound foi separado do repositório inbound em `app/database/totvs_outbound_repository.py`, evitando que os testes de fronteira interpretem a leitura de fatos como reimplementação do apontamento.
- `TotvsOutboundService` lê um fato canônico por ID, gera `ProductionAppointment` ou `StopReport` e delega o envio ao gateway; não conhece `OperatorFlowService`, máquina de estados ou origem da OP.
- `TotvsWspcpClient` exige endpoint, namespace do WSDL e configuração explícita; o código não usa namespace padrão inventado.
- O script `scripts/homologar_totvs_outbound.py` possui dry-run por padrão e travas para banco `gestor_pecas_test`, host esperado, endpoint terminado em `/WSPCP.apw`, confirmação literal de TESTE, timestamp não futuro, motivo explícito e bloqueio de retrabalho.
- O dry-run do evento canônico 186 gerou `ProductionAppointment` preservando OP `A9717001001`, operação `10` e recurso `ROBO P`; nenhuma mensagem foi transmitida.

Reusable knowledge:

- O recurso industrial é preservado de `catalogo_operacoes_op.totvs_machine_code`; o mapper não substitui `MachineCode` pelo nome do posto visual.
- Boas e refugo são grandezas separadas; `ReportQuantity` é boas + refugo, sem retrabalho.
- Refugo exige `WasteCode` TOTVS explícito; texto ou código do Gestor não é convertido automaticamente.
- A configuração do namespace deve vir do WSDL real do ambiente. O `.env.example` foi alterado para deixar `GESTOR_TOTVS_OUTBOUND_SERVICE_NAMESPACE` vazio até a TI fornecer o valor.

References:

- `mes/integrations/totvs/outbound_models.py`
- `mes/integrations/totvs/outbound_mapper.py`
- `mes/integrations/totvs/outbound_ack.py`
- `mes/integrations/totvs/outbound_service.py`
- `backend/integrations/totvs_wspcp.py`
- `app/database/totvs_outbound_repository.py`
- `scripts/homologar_totvs_outbound.py`
- Dry-run: `C:\Python314\python.exe scripts\homologar_totvs_outbound.py --event-id 186 --contract productionappointment --allow-zero-quantity`

## Task 3: Testes, build e documentação

Outcome: success

Key steps:

- Testes específicos outbound: 14/14 aprovados.
- Testes de fronteira outbound/arquitetura: 22/22 aprovados após corrigir uma referência textual indevida a `OperatorFlowService` no docstring dos DTOs.
- Suíte Python completa: 455 testes aprovados, 1 pulado explicitamente porque o banco TESTE ativo não possui fatos na janela histórica de julho/2026. A execução terminou com `OK (skipped=1)`.
- Suíte Web: 46/46 aprovados com `npm test`.
- Build React/TypeScript aprovado com 380 módulos transformados via `npm run build`.
- `ProductionOrder` e `WhoIs` permaneceram preservados pelos testes de contrato/regressão.
- Foram corrigidos dois testes dependentes de dados temporários: uma data fixa `26/08/2026` foi substituída pela data corrente; o teste de julho passou a pular explicitamente quando a massa histórica não existe. Essas correções não alteraram regra produtiva.
- Atualizados `ROADMAP.md`, `AGENTS.md` e criada a documentação `docs/INTEGRACAO_TOTVS_OUTBOUND_ETAPA5.md`, registrando status PARCIAL e os bloqueios de homologação.

Failures and how to do differently:

- Avisos de rate limit da IA, timeout simulado do Telegram e exceções injetadas de persistência apareceram na suíte completa, mas foram cenários deliberadamente testados; a execução final terminou aprovada.
- O teste de equivalência de OEE não deve exigir uma janela histórica inexistente no banco ativo; preservar skips explícitos condicionados à massa disponível, sem fabricar dados.

References:

- `C:\Python314\python.exe -m unittest discover -s tests -q` → `Ran 455 tests ... OK (skipped=1)`
- `npm test` em `web` → `6 test files passed; 46 tests passed`
- `npm run build` em `web` → build aprovado, 380 módulos transformados
- `ROADMAP.md` seção `### ETAPA 5 — Retorno Gestor → TOTVS / ciclo de vida da OP [PARCIAL — 31/08/2026]`

## Task 4: Homologação prática no TOTVS TESTE

Outcome: partial

Preference signals:

- O usuário exigiu que a etapa só terminasse após ACK real e prova antes/depois no TOTVS TESTE -> não declarar sucesso com dry-run, testes unitários ou histórico do PCPA112.
- O usuário pediu para parar objetivamente quando fosse necessária ação manual e continuar o restante da implementação -> implementação e testes foram concluídos, deixando apenas os dados ambientais pendentes.

Key steps:

- TOTVS TESTE foi identificado no Chrome como `TOTVS Manufatura MSSQL Csed4j_dev`, empresa/filial `Gts do Brasil Ltda / Filial_iv - Verticalizacao`.
- PCPA112 foi consultado somente em leitura; não foram acionados excluir, reprocessar, envio ou alterações no TOTVS.
- Nenhuma OP foi enviada. `A9717001001` foi usada somente em dry-run; `A9716901001`, `A9717001001` e `A9717101001` não foram consideradas descartáveis sem autorização da Manufatura/TI.
- O banco real `gestor_pecas` e o TOTVS REAL não foram acessados/alterados.

Failures and how to do differently:

- A homologação Gestor → WSPCP não pôde começar porque faltam quatro informações externas: URL/porta do listener WSPCP TESTE, namespace/SOAPAction do WSDL, OP descartável autorizada com empenhos válidos e códigos de motivo de parada/refugo.
- Ainda não há ACK real, registro emitido pelo Gestor no PCPA112 nem comparação antes/depois no MATA650. Portanto, os efeitos sobre `C2_DATRF`, quantidade acumulada e cada legenda continuam não verificados para uma mensagem do Gestor.

Reusable knowledge:

- A próxima continuação deve solicitar somente: URL completa terminada em `/WSPCP.apw`, hostname esperado, namespace e eventual SOAPAction; não solicitar senha pelo chat.
- A Manufatura/TI deve indicar uma OP TESTE descartável, firme, liberada, com empenhos válidos, quantidade pequena, operação e recurso válidos, além de códigos SX5 grupo 44 para parada e código TOTVS de refugo.
- Depois disso, executar cenários pequenos A–F, registrar antes no MATA650/PCPA112, gerar evento canônico, fazer dry-run, enviar somente com `--send` e confirmação exata, registrar ACK, consultar depois e marcar CONFIRMADO ou DIVERGENTE.
- Não iniciar outbox, retry permanente, worker, reconciliação automática ou próxima etapa antes de fechar o gate prático.

References:

- Bloqueio documentado em `docs/INTEGRACAO_TOTVS_OUTBOUND_ETAPA5.md`, seção “Ação manual necessária”.
- Relatório final: `ETAPA 5 CONCLUÍDA: NÃO`.
- Pendências exatas: URL WSPCP TESTE; hostname/namespace/SOAPAction; OP descartável; código SX5/44 de parada; código de refugo; ACK e prova MATA650/PCPA112 antes/depois.
