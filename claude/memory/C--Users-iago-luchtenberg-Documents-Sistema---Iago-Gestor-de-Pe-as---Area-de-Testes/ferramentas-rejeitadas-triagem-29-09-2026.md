---
name: ferramentas-rejeitadas-triagem-29-09-2026
description: "Triagem 29/09/2026: Plandex, taste-skill, Graft e TypeSafe/Jev rejeitados, com motivo. Strix adotado só sob demanda. Não reavaliar do zero."
metadata:
  type: project
---

Rejeitados pelo usuário em 29/09/2026:
- **Plandex**: agente standalone com sandbox de diff e contexto de 2M tokens. O git/worktree já cobre o sandbox, e seria um 5º agente sem sync. A versão Cloud acabou em 10/2025. Reavaliar só se uma refatoração estourar o contexto de todos os agentes atuais.
- **taste-skill** (leonxlnx): conflita com o contrato de design do Gestor (hoje `DESIGN.md`), e o `impeccable` já cobre esse papel.
- **Graft** (trailhq): duplica o graphify.
- **TypeSafe/Jev**: não otimiza a saída do Claude. É uma skill para construir apps sobre os modelos "System One" da TypeSafe, com conta e chave próprias.

Adotado: **Strix** (usestrix), pentest com agentes, só sob demanda. Ver [[strix-sob-demanda]].

**Why:** evitar que alguém reavalie do zero as mesmas ferramentas.
**How to apply:** se uma delas reaparecer, citar este motivo e só reabrir com informação nova.
