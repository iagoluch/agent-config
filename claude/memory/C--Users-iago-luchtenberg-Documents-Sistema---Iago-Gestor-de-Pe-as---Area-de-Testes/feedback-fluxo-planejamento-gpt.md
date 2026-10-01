---
name: feedback-fluxo-planejamento-gpt
description: "O usuário planeja/discute as próximas Waves com o GPT antes de trazê-las para implementação aqui — conteúdo de wave futura vindo do GPT não é invenção, é planejamento real ainda não iniciado neste repositório"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cf9cf250-080d-46c0-be6f-81d695cbf05f
  modified: 2026-09-14T12:24:50.228Z
---

O usuário tem um fluxo de trabalho de duas etapas: planeja e discute o desenho de cada Wave nova em conversas com o GPT, e só depois traz essa Wave para esta conta (Claude Code) para implementação de fato.

**Why:** em 2026-09-14 eu (Claude) marquei uma "Wave 6I" citada num relatório do GPT como "invenção/fabricação", porque ela não aparecia em nenhum documento do repositório (`ROADMAP.md`). O usuário corrigiu: não é invenção — é uma wave real que estava sendo desenhada no GPT e ainda não tinha sido trazida para cá, por isso não existe implementação nem registro no ROADMAP ainda. Ver [[wave6cde-estado]] para o histórico real das waves já implementadas (6A-6E, todas concluídas 11/09/2026) — a 6I é a continuação natural, ainda pendente de início.

**How to apply:** quando o usuário trouxer um plano/relatório de outra IA (GPT ou outra) descrevendo uma wave/etapa **futura** que ainda não está no código deste projeto, não tratar automaticamente como erro/alucinação só por não bater com o estado atual do repo — perguntar ou assumir que é planejamento em andamento, e verificar separadamente se o conteúdo sobre o **estado passado/já implementado** está correto (esse sim deve ser cruzado com o código real). A checagem factual contra o repositório vale para "o que já existe", não para "o que ainda vamos fazer".
