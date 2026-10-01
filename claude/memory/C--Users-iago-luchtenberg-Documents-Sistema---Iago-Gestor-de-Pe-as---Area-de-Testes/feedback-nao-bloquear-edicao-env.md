---
name: feedback-nao-bloquear-edicao-env
description: Não propor/implementar hook que bloqueia edição do .env neste projeto — usuário precisa editá-lo livremente para evoluções futuras.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 75a23e2d-e8c2-44ad-b03f-c9289219fc68
  modified: 2026-09-20T23:57:07.066Z
---

Não sugerir nem implementar um hook `PreToolUse` bloqueando edição de `.env` no Gestor de Peças.

**Why:** o usuário disse explicitamente (20/09/2026) que precisa manter a edição do `.env` habilitada para evoluções futuras do projeto — mesmo sabendo que o arquivo contém segredos reais (motivo pelo qual o skill `claude-automation-recommender` sugeriu o hook na sessão anterior).

**How to apply:** se uma futura recomendação de automação (auditoria, `claude-automation-recommender`, revisão de segurança) sugerir bloquear/restringir edição de `.env`, mencionar essa preferência já registrada em vez de implementar o bloqueio. Isso não muda a orientação geral de nunca colocar segredos em URL/logs — só a decisão específica de não travar a edição do arquivo via hook.
