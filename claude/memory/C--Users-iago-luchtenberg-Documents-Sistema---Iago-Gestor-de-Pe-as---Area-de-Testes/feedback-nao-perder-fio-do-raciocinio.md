---
name: feedback-nao-perder-fio-do-raciocinio
description: "Usuário corrigiu: pedi de novo um número de OP que já estava óbvio pelo contexto imediato da conversa"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T19:49:05.100Z
---

Ao continuar um plano que o próprio usuário acabou de colar (ex.: instruções
vindas de outra sessão/IA), ler o contexto imediato da conversa antes de
pedir informação que já foi estabelecida — não tratar o texto colado como se
fosse um início de conversa do zero.

**Why:** em 23/09/2026, o usuário colou um plano de teste (comparar
`StatusOrderType` antes/depois de excluir uma OP no Protheus) que pedia "me
passe o número da OP". Eu pedi um número novo, ignorando que a OP relevante
(`VAAAC801001`) já era o assunto ativo da conversa há várias mensagens —
tinha acabado de ser puxada, sincronizada e usada como base do próprio plano
de teste. O usuário teve que corrigir: "vai ser com essa OP que usamos
agora, creio que você se perdeu no raciocínio, não quero que isso ocorra
novamente."

**How to apply:** antes de fazer uma pergunta que parece "óbvia demais" dado
o que já foi discutido, checar se a resposta já está no contexto recente da
própria conversa — especialmente quando o usuário cola texto de outra fonte
que reaproveita um plano já em andamento aqui.
