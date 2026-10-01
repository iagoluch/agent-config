---
name: gap-status-order-type-exclusao-op-23-09-2026
description: "23/09/2026: testado o que acontece quando uma OP puxada via GPOPSYNC é excluída no Protheus — vira 404 (nao_encontrada), não StatusOrderType diferente; usuário considerou cenário raro e fechou o teste"
metadata:
  node_type: memory
  type: project
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T19:58:47.562Z
---

Testado em 23/09/2026: puxar uma OP via pull sob demanda (GPOPSYNC), anotar
o `StatusOrderType` (sempre `"1"`), excluir a mesma OP no Protheus TESTE, e
puxar de novo para comparar.

**Resultado:** a OP excluída não volta com `StatusOrderType` diferente — o
Protheus faz o que parece ser hard delete real da linha, e o GPOPSYNC passa
a devolver 404 (`status=nao_encontrada`). Testado com `VAAAC801001` (filial
`010001`); confirmado que não há como comparar "antes/depois" porque não
existe "depois" com dado — só ausência.

Efeito no Gestor de Peças: nenhum risco identificado. O pull sob demanda só
consulta o Protheus para OPs que ainda não existem localmente
(`lookup_local` responde antes de qualquer chamada de rede) — então excluir
uma OP no Protheus *depois* dela já estar sincronizada no Gestor não afeta o
registro local de forma nenhuma.

**Decisão do usuário (23/09/2026):** exclusão de OP no Protheus é cenário
raro na prática. O cenário real mais provável é **fechamento de uma OP no
meio do roteiro** (um recurso concluído, OP ainda ativa) — e o usuário
concluiu que isso não deve afetar nem atrapalhar o fluxo do Gestor de Peças.
Teste fechado, sem pendência de código.

**Why:** evita reabrir essa investigação (StatusOrderType/exclusão de OP) à
toa; já foi testado empiricamente e o resultado é conhecido.

**How to apply:** se essa dúvida voltar, apontar direto pra este achado —
excluir OP no Protheus = 404 daqui pra frente, sem diferenciação de status;
não é bug, é o comportamento observado do lado do Protheus.
