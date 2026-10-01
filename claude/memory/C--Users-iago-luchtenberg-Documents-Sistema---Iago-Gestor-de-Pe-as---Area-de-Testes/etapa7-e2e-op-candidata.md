---
name: etapa7-e2e-op-candidata
description: OP escolhida e restrições de ambiente levantadas para o E2E da Etapa 7 (reconhecimento em 02/09/2026, nada executado ainda).
metadata:
  type: project
---

Reconhecimento da Etapa 7 (E2E/resiliência/reconciliação) feito em 02/09/2026. **Nenhuma execução, nenhuma escrita.** Achados que economizam a redescoberta:

**OP principal escolhida: `PCMIXQ01001`** — única candidata que cruza TOTVS + SigmaNEST + operador + marco terminal.
- TOTVS TESTE, filial `010004`, produto `PNT002002003`, planejado 48, roteiro 35, `status_pcp='1'` (aberta), inbox id 22.
- Roteiro projetado: `10/PLASMA/Corte` (activity 108761), `20/CNC-01/Usinagem` (activity 160893), `99/ALMOX4` marco terminal inativo (activity 128285).
- **Zero apontamentos no Gestor** — base limpa para o E2E.
- SigmaNEST: `Wo.WONumber = PCMIXQ01001`, tarefa `T3226`, máquina `Messer_XPR_300`, 9 nestings (7975–7982, 8312), **todos com `CompDate` preenchido (julho/2026)** — exercita a regra "concluído na origem: esconde da fila, não aponta, não finaliza OP".

**Restrição decisiva: não existe acesso programático ao banco Protheus.** `C2_QUJE`, `C2_DATRF`, legenda e PCPA112 foram conferidos manualmente na UI nas etapas anteriores. Para a reconciliação, o lado TOTVS só pode vir de (a) ACK/InternalId da outbox e (b) `ReportQuantity`/`StatusOrderType` do `ProductionOrder` reingerido — o parser já lê `report_quantity`, mas ele **não é persistido** em `catalogo_pcp_ops`; está disponível no `payload_raw` da inbox.

**PCPA109 não pode ser disparado por mim** (sem acesso à UI Protheus). O inbound real deve ser exercitado por POST SOAP no endpoint próprio do Gestor (`POST /PcfIntegService`, SOAPAction `http://tempuri.org/EAIService/receiveMessage`) com payload Protheus autêntico da inbox.

Ambiente conferido: PostgreSQL `gestor_pecas_test` schema 19 OK; WSPCP TESTE WSDL responde HTTP 200; SigmaNEST TCP OK; backend/túnel desligados. `GESTOR_EXPECTED_DATABASE=gestor_pecas_test` protege o banco REAL de qualquer `Database()` não-teste.

Códigos TOTVS já homologados a usar: `StopReasonCode` `0010`/`0018`, `WasteCode` `RP`. Ver [[etapa7-plano-execucao]].
