---
id: 4
title: "Skill ou agente que depende so da descricao nao dispara; so o que tem hook e usado"
status: actioned
type: cross-cutting
skill: ["llm-council", "skill-router"]
proposes_skill: 
target_file: ["~/.claude/CLAUDE.md", "~/.claude/hooks/workforce-routing-reminder.sh"]
siblings_checked: "ponytail e task-observer (com hook) = 15 e 31 usos; llm-council, skills de fluxo e 26 funcionarios = 0-2 usos em set/2026"
area: "ativacao de skills e subagentes"
date: 2026-09-29
session_context: "Usuario notou llm-council e workforce sem uso; contagem nos .jsonl de 166 sessoes de set/2026"
resolved: 2026-09-29
resolution: "hook UserPromptSubmit global de roteamento + autorizacao permanente no CLAUDE.md + linha de visibilidade 'Roteamento:'"
reference: "memory/feedback-delegacao-e-council-autorizados.md"
---

Descricao com "trigger AUTOMATICALLY" nao basta quando o ambiente e outras regras puxam no sentido contrario (instrucao de nao abrir subagente sem pedido, regras de economia). O principio geral: toda skill ou rota que o usuario quer usada por padrao precisa de um gatilho mecanico (hook) e de uma saida visivel que prove o disparo. Revisao futura: medir de novo as contagens por .jsonl (council, subagent_type) depois de 1-2 semanas.
