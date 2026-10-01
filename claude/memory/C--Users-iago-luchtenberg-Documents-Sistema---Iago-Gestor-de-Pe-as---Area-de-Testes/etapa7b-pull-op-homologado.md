---
name: etapa7b-pull-op-homologado
description: "Etapa 7B (03/09/2026): pull real de OP sob demanda homologado via GPOPSYNC/MATI650 (rotina AdvPL customizada), superando o bloqueio da Etapa 6.1"
metadata: 
  node_type: memory
  type: project
  originSessionId: cf9cf250-080d-46c0-be6f-81d695cbf05f
  modified: 2026-09-14T20:11:47.141Z
---

Em 03/09/2026, um dia depois de a Etapa 6.1 provar que os mecanismos **padrão** do Protheus não suportam pull de OP (ver [[etapa61-totvs-sem-pull-de-op]]), a Etapa 7B homologou um caminho real usando uma rotina AdvPL **customizada**: `GPOPSYNC.prw` (`WSRESTFUL gestorpecaspo`, endpoint `:1467`), que aciona `MATA650PPI → PCPa650PPI → MATI650` (a mesma cadeia oficial que gera o `ProductionOrder`, ver [[protheus-fontes-1212510]]) e devolve o XML em memória — sem precisar publicar a OP como transação EAI genérica.

**Comprovado com OP real no banco `gestor_pecas_test`:**
- OP `00615903001`: fluxo completo `OrderProvisioningService → ProductionOrderOnDemandSyncService → GPOPSYNC → MATI650 → TotvsProductionOrderIngestionService → PostgreSQL → consulta operacional`. Chamada HTTP real, 1,317s, HTTP 200, `ProductionOrder` 2.004 real com roteiro completo (4 atividades, 1 operação apontável + marco terminal 99 inativo).
- OP `10795102002`: caso de cabeçalho sem roteiro (`ListOfActivityOrders` vazio) — o Gestor não inventa operações; responde `sem_roteiro`/`found=false` em vez de travar em timeout, e não repete a chamada ao ERP em consultas seguintes.
- Idempotência confirmada: segunda consulta é local, zero chamada adicional ao ERP.

**Etapas seguintes na mesma sequência (03/09/2026):**
- Etapa 7C: apontamento de Qualidade (`INSPECAO`) implementado como capacidade de setor (Dobra/Usinagem/Serra, Corte fora), fila local (não aciona GPOPSYNC), migration 21.

**Why:** evita redescobrir/reabrir a investigação de pull de OP como se ainda fosse um bloqueio — não é mais. O bloqueio real hoje é só o **contrato de descrição de roteiro/operação** dos serviços padrão do Protheus, contornado pelo `GPOPSYNC` customizado.

**How to apply:** quando o assunto for pull de OP sob demanda, tratar como **implementado e homologado**, não como pendência. Não montar `ProductionOrder` manualmente fora do `GPOPSYNC`. Fonte completa: `ROADMAP.md` linhas ~975-1046 (Etapas 7A/7B), evidências em `docs/evidencias/TOTVS_ETAPA7B_HOMOLOGACAO_REAL_2026-09-03.md`.

**Correção 14/09/2026 (confirmado pelo usuário):** o `GPOPSYNC` é o **canal principal e mais usado** de entrada na prática — não um fallback secundário. O receptor SOAP passivo `PcfIntegService` (push do Protheus) existe no código e responde, mas o usuário **não usa mais** esse caminho na operação real. Ao explicar a integração (docs, diagramas, respostas), dar ênfase ao GPOPSYNC como o mecanismo em uso; mencionar o PcfIntegService apenas como legado/existente, não como canal ativo.
