---
name: feedback-uso-amplo-de-skills
description: "Usuário quer uso pleno e automático de todas as skills instaladas em ~/.claude, em qualquer projeto, sem que uma atrapalhe a outra"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b4f59e19-62d2-48e5-9538-24c0d38de74d
  modified: 2026-09-13T21:23:34.823Z
---

Usar automaticamente todas as skills relevantes disponíveis na raiz do Claude (`~/.claude/skills/*`), conforme a demanda de cada tarefa, em todos os projetos — não só neste. Isso é uma extensão de [[feedback-ponytail-toda-tarefa]] (ponytail continua obrigatória em toda tarefa de código) somada ao roteamento já descrito em `~/.claude/CLAUDE.md` (seção "Claude Code — Skill Routing Configuration").

**Why:** o usuário quer aproveitar o ecossistema completo de skills instaladas, não um subconjunto memorizado, e enxerga isso como ter "um cérebro literalmente" — ou seja, o roteamento entre skills deve ser automático e transparente, sem ele precisar pedir skill por skill.

**How to apply:**
- Antes de agir, identificar quais skills instaladas em `~/.claude/skills/` se aplicam à tarefa (código, review, testes, git, docs, integrações, etc.) e carregá-las via Skill tool conforme o roteamento já definido no CLAUDE.md global.
- Combinar múltiplas skills apenas quando a tarefa realmente cruzar domínios (ex.: debugging + testes; API design + frontend).
- Nunca deixar uma skill sobrescrever ou quebrar o comportamento de outra: se duas skills conflitarem (ex.: uma pede investigação exaustiva e outra pede o caminho mínimo), priorizar a que for mais específica ao domínio da tarefa atual e manter o resultado funcional — não travar a execução por causa do conflito.
- Não anunciar rotineiramente qual skill foi escolhida, a menos que isso ajude a explicar uma decisão técnica.
- Isso não substitui nem enfraquece as regras de economia de tokens já registradas em [[feedback-economia-de-tokens]] — usar mais skills não significa investigar mais fundo do que o necessário.
