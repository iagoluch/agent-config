---
name: feedback-nao-fragmentar-em-agentes-em-massa
description: "usuário corrigiu o disparo de 4 agentes paralelos para uma auditoria — mesmo quando o escopo parece dividível, preferir um único agente coerente"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T14:45:31.077Z
---

Mesmo diante de uma tarefa de investigação enorme e multi-domínio (ex.: auditoria adversarial de um MES cobrindo dados, segurança, integrações, frontend), não fragmentar em vários agentes paralelos por padrão. O CLAUDE.md global já tem a seção "Delegation efficiency" dizendo para preferir um agente primário único quando a tarefa pode ser dona de forma coerente por um só, e usar múltiplos apenas quando há workstreams genuinamente independentes que se beneficiam de paralelismo — mas na prática, mesmo uma auditoria por "fluxos ponta a ponta" (que parecia justificar divisão por domínio) foi considerada fragmentação em massa indevida pelo usuário.

**Why:** usuário interrompeu explicitamente ("pare, lembre do que eu falei sobre os agentes em massa") ao ver 4 agentes `extreme` disparados de uma vez para uma auditoria. Reforça [[limpeza-skills-composio-automation]]-style de preferência por economia e a instrução já existente sobre não duplicar investigação entre múltiplos tiers de modelo.

**How to apply:** para tarefas grandes de investigação/auditoria, mesmo multi-domínio, começar com UM agente (ou fazer inline) a menos que o usuário peça explicitamente paralelismo, ou que haja uma razão concreta e não-óbvia (ex. artefatos massivos que não cabem em um único contexto). Se a tarefa realmente exigir mais de um agente, perguntar ou justificar antes de disparar múltiplos de uma vez — não presumir que "dividir por fluxo" é diferente de "agentes em massa" aos olhos do usuário.

**Escopo esclarecido em 29/09/2026:** esta regra limita *fan-out* (vários agentes em paralelo numa tarefa), não a delegação em si. Rotear trabalho R1+ para o owner único da matriz e rodar `llm-council` em decisão com tradeoff estão autorizados permanentemente — ver [[feedback-delegacao-e-council-autorizados]].
