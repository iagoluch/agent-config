---
name: limpeza-skills-composio-automation
description: 832 skills *-automation (Composio) removidas do ~/.claude/skills por não terem uso e não mapear pro stack do usuário
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1c47680b-3899-4e29-a9c3-4bb90c0a739d
  modified: 2026-09-20T18:37:12.931Z
---

Em 20/09/2026, removidos 832 symlinks de skills `*-automation` (pacote `composio-skills`: Slack, Notion, HubSpot, Zoho, etc.) de `~/.claude/skills`. Confirmado por evidência de uso real (grep nos históricos de sessão): 0 invocações em nenhuma delas, contra uso real de `ponytail`, `artifact-design`, `docx`, `loop`.

**Why:** o usuário confirmou que não usa nenhum SaaS genérico (Slack/Notion/Sheets/e-mail automatizado) no fluxo de trabalho — todo o projeto roda sobre sistemas proprietários (TOTVS/Protheus, SigmaNEST, Andon, WSPCP/SOAP) que não existem no catálogo Composio. Manter esses 832 conectores só adiciona ruído a cada listagem de skills sem nenhum ganho.

**How to apply:** não reinstalar/re-linkar essas automações a menos que o usuário mencione explicitamente passar a usar um SaaS coberto pelo catálogo (Slack, Notion, Google Sheets, etc.). O pacote fonte continua intacto em `~/.claude/skills/composio-skills/` — restaurar é rodar `configure-skills.bat` de novo, symlink por symlink se precisar de só uma. As ~45 skills de engenharia reais (incremental-implementation, debugging-and-error-recovery, TDD, etc.) e a família `ponytail` foram mantidas — são a base do roteamento automático do CLAUDE.md do usuário, custam pouco e continuam relevantes independente de invocação explícita.

Achado à parte (não resolvido): o marketplace de plugins deste Claude Code (`~/.claude/plugins/known_marketplaces.json`) aponta `installLocation` para `C:\Users\logistica.unidade4\...`, sugerindo que esta máquina já teve outro perfil de usuário Windows configurando Claude Code. Existem 5 skills não rastreadas (`contexto`, `decidir`, `dia`, `fim`, `status`) cuja origem não foi encontrada em `~/.claude/skills` nem no marketplace oficial — ficaram intocadas até confirmação do usuário.
