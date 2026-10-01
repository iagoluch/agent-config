#!/usr/bin/env bash
# UserPromptSubmit hook (global): lembra o roteamento da IA Workforce e do llm-council
# a cada prompt. Skills e agentes que dependem so de descricao nao disparavam (0 usos
# em set/2026); este hook e o gatilho mecanico. Nao bloqueia; so injeta contexto.
cat >/dev/null
echo "Roteamento (hook): conversa casual ou pergunta factual -> responda direto. Tarefa -> classifique R0-R3 (CLAUDE.md global). R0/R1 clara em 1-3 arquivos -> avalie handoff Nemotron. R1+ -> delegue ao owner da .ai/ROUTING_MATRIX.md e carregue a skill de fluxo (skill do projeto em .claude/skills tem prioridade sobre a tabela Task-to-skill generica); R2/R3 -> + qa-test-engineer/technical-reviewer. Decisao com tradeoff real entre opcoes -> skill llm-council. Delegacao e council autorizados permanentemente pelo usuario. Feche a resposta com: 'Roteamento: R<n> · <agentes|direto|Nemotron> · skills <lista|nenhuma>'."
exit 0
