---
name: feedback-task-observer-ativacao
description: "Skill task-observer instalada globalmente e ativada de verdade (hook SessionStart global + instrução no CLAUDE.md global), não só por description-match"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f960d4d6-ae46-465d-83b1-a4485978d1b2
  modified: 2026-09-22T12:57:16.808Z
---

Usuário baixou e pediu instalação da skill `task-observer` ("One Skill to Rule Them All", github.com/rebelytics/one-skill-to-rule-them-all) em 22/09/2026, instalada globalmente em `~/.claude/skills/task-observer/`. É um sistema de observação contínua de melhorias de skill (loga correções/padrões em `observation-log/`, revisão semanal, etc.).

A própria skill afirma que description-matching sozinho não é confiável (é a camada mais fraca das 4 que ela documenta em `references/environments.md`); recomenda hook de `SessionStart` como única camada realmente enforced.

**Why:** ao perguntar ao usuário se deixava só description-match ou configurava ativação real (mesmo padrão usado para [[feedback-ponytail-toda-tarefa]] e headroom), ele escolheu explicitamente "2" — configurar ativação real.

**How to apply — o que foi feito (22/09/2026):**
- `~/.claude/hooks/task-observer-activate.sh` — hook `SessionStart` GLOBAL (não por projeto, diferente do ponytail/headroom que são hooks locais deste projeto) que injeta `additionalContext` pedindo para invocar `Skill({skill:"task-observer"})` e rodar o Session Start Protocol antes da primeira tool call/plano de qualquer sessão, em qualquer projeto.
- Wireado em `~/.claude/settings.json` (global, não tinha bloco `hooks` antes — criado do zero).
- Instrução redundante adicionada em `~/.claude/CLAUDE.md` (seção "# task-observer"), por ser a doc que a própria skill recomenda como segunda camada.
- Escopo é GLOBAL porque a skill foi instalada globalmente (`~/.claude/skills/`), diferente de ponytail/headroom que são regras só deste projeto (Gestor de Peças).
- Não commitado no repo do projeto — os arquivos alterados (`~/.claude/settings.json`, `~/.claude/CLAUDE.md`, `~/.claude/hooks/task-observer-activate.sh`) ficam fora do git deste projeto.
- Postura padrão da skill é "log-and-defer": não oferecer "aplicar agora vs. adiar" a cada observação registrada; só agir em sessão nos 3 gatilhos que ela mesma define.
