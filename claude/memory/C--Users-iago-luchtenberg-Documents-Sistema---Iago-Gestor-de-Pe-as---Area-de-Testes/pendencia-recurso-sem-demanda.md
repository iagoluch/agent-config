---
name: pendencia-recurso-sem-demanda
description: "IMPLEMENTADO em 2026-09-13 — recursos fora de turno sem demanda agora mostram estado explícito 'recurso sem demanda' em vez de parada"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-13T21:05:23.439Z
---

**STATUS: implementado em 2026-09-13** por agente em background. Fonte única: `ManufacturingRules.resource_has_no_demand` em `mes/domain/manufacturing_rules.py`, avaliada uma vez em `consulta_operacional` (produtor canônico do estado de recurso), usando o calendário por recurso da Wave 6A. Andon agora mostra esse estado próprio, sem cor/classificação de parada; `physical_category` preserva o estado persistido; nenhuma migration (é leitura derivada). Coberto por testes (parte dos 257 testes de backend que passaram, incluindo suite de manufacturing_rules).

Pedido original abaixo, mantido como referência:

Usuário teve essa ideia em 2026-09-13, observando o `/simulation-observatory` ao vivo: quando a fábrica está **fora de turno** (fora de 08:00-17:30 e sem HE ativa) e ninguém está trabalhando, os recursos deveriam ser exibidos com um estado dedicado — **"recurso sem demanda"** — em vez do que aparecem hoje.

**Contexto de negócio já estabelecido** (ver seção 16 do documento de simulação e [[wave6-estado]]): "Fora de turno sem HE não deve virar automaticamente uma parada não planejada." Ou seja, já existe a preocupação de não classificar erroneamente um recurso ocioso fora de turno como parada não planejada (vermelho). A ideia nova do usuário é ir além: dar a esse caso um **rótulo/estado próprio e explícito** ("recurso sem demanda"), distinto de qualquer estado de parada (planejada ou não) e distinto de "ocioso dentro do turno" — para deixar claro visualmente (Andon, observatório, gestão) que o recurso não está parado por problema, só não há demanda/turno naquele momento.

**Why:** o usuário pediu para implementar isso "imediatamente após a simulação" — ele quer priorizar essa melhoria assim que a simulação industrial prolongada (rodando em background em 2026-09-13) terminar, mas não quis interromper a simulação para implementar agora.

**How to apply:** quando o usuário retomar este item, localizar onde os estados de recurso são calculados/exibidos (Andon, `/simulation-observatory`, telas de gestão/operador) e onde a regra "fora de turno sem HE ≠ parada não planejada" já está implementada (Wave 6A/6B), e adicionar o estado explícito "recurso sem demanda" para esse cenário, sem quebrar a distinção existente entre parada planejada/não planejada. Confirmar com o usuário se esse estado deve aparecer em todas as telas (Andon, dashboards, observatório) ou só nas que ele especificar.
