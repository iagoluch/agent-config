---
name: etapa61-totvs-sem-pull-de-op
description: "SUPERADA em 03/09/2026 pela Etapa 7B: pull de OP real via GPOPSYNC/MATI650 foi homologado com sucesso. Ver [[etapa7b-pull-op-homologado]]."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4c1c2f3e-cfa7-43f4-81db-7ea6d3c7d9ba
  modified: 2026-09-14T12:16:11.272Z
---

**ATUALIZAÇÃO 2026-09-14: esta memória está DESATUALIZADA — não tratar como fato atual.** O "fato novo" que ela dizia faltar aconteceu no dia seguinte (03/09/2026, Etapa 7B): pull real de OP via `GPOPSYNC/MATI650` foi construído e homologado com sucesso (OP real `00615903001`, HTTP 200 em 1,3s, dados completos incluindo roteiro). O conteúdo original abaixo (02/09/2026) só prova que os mecanismos **padrão** do Protheus (`WSPCP` nativo, `MTPRODUCTIONORDER`, `MTINTEGRATIONAPS`, REST de cabeçalho) não servem — o que continua verdadeiro — mas isso foi contornado com uma rotina AdvPL customizada (`GPOPSYNC.prw`, endpoint `WSRESTFUL gestorpecaspo`) publicada no Protheus. Ver [[etapa7b-pull-op-homologado]] para o estado real e [[protheus-fontes-1212510]] para a cadeia técnica.

---

**Conteúdo original (histórico, parcialmente superado):**

O Protheus (TOTVS TESTE `CSED4J_DEV`, `gtsdo143182…`) **não** possui mecanismo
suportado para o Gestor pedir uma OP e receber um `ProductionOrder`. Provado por
resposta do próprio ambiente em 02/09/2026:

- `WSPCP.apw` implementa **só** `productionappointment` e `stopreport`;
  `ProductionOrder` → *"Transação PRODUCTIONORDER não implementada"*.
- EAI genérico ativo, mas o app host `CSED4J_DEV01@PROTHEUS` tem 11 adapters
  (`orderassignmentsinformation`, `paymentcondition`, `project`, `request`) e
  **nenhum** `ProductionOrder`; nenhuma aplicação externa cadastrada.
- `GET /rest/totvseai/standardmessage/v1/contents/{transaction}` → HTTP 500 para
  toda transação.
- `MTPRODUCTIONORDER` / `MTINTEGRATIONAPS` — validados a fundo em 02/09/2026 e
  **descartados (decisão C)**, por três bloqueios independentes:
  (a) `PRTCHKUSER : WebService invalido para este login` (mas `GETHEADER` no
  mesmo serviço responde 200 → é liberação por método/usuário, e o fault não
  muda com nenhum `USERCODE` → depende do login HTTP);
  (b) sem parâmetro de empresa/filial no WSDL e `tenantId` ignorado — a
  publicação é `01/010001` e as OPs são `01/010004`;
  (c) **decisivo** — `PRODUCTIONORDERVIEW` não traz roteiro nem descrição de
  produto (`ItemDescription` é obrigatório no parser) e `POOPERATION` não traz
  descrição de operação. A assinatura do mapper canônico é
  `(ActivityCode, ActivityDescription, WorkCenterCode, MachineCode)`; apagando
  só a descrição no `ProductionOrder` real de `1079689C001`, o mapper passa de
  `[('10','LASER1'),('99','ALMOX4')]` + 1 marco terminal para `[]` + 0.
- REST `/rest/api/pcp/v1/productionOrders` (porta **1467**) funciona com a
  credencial REST, mas devolve só cabeçalho, sem roteiro, e ignora
  `tenantId: 01,010004`.
- `FWHOSTCOMMUNICATION.RUNMETHOD` é host↔host Protheus com `FwSerializable`; não
  aciona `PCPA111::sincOP()` de forma suportada.

**Why:** essa investigação custou uma sessão inteira e o resultado é negativo —
repeti-la desperdiça tempo e bate no ERP sem ganho.

**How to apply:** tratar como fato até haver mudança no Protheus. Não repetir a
validação dos serviços padrão de OP: liberar `PRTCHKUSER` ou publicar para
`010004` não resolve, porque o contrato não tem as descrições. A busca sob
demanda já está implementada e homologada no Gestor; ela só liga quando
`GESTOR_TOTVS_OP_PULL_ENDPOINT` apontar para a rotina que a TI/TOTVS precisa
publicar (contrato em `docs/INTEGRACAO_TOTVS_OP_SOB_DEMANDA_ETAPA61.md` §3).
Nunca montar `ProductionOrder` à mão a partir de SC2/SG2/SHY ou das APIs REST de
cabeçalho. Ver também [[etapa7-e2e-op-candidata]].

Descoberta útil de ambiente: o índice completo de web services fica em
`https://gtsdo143182.protheus.cloudtotvs.com.br:1465/ws/` (228 serviços) e o de
REST em `…:1467/rest/` com login por form (`__USER`/`__PSW`).
