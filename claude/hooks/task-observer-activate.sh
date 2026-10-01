#!/usr/bin/env bash
# SessionStart hook (global): injeta o gatilho de ativacao da skill task-observer
# em toda sessao, em qualquer projeto. Nao bloqueia; so injeta contexto.
cat << 'JSON'
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"Antes da primeira chamada de ferramenta desta sessao (e antes de propor qualquer plano): invoque a skill 'task-observer' (Skill({skill:\"task-observer\"})) e execute seu Session Start Protocol (checagem de storage, varredura de frontmatter do observation-log, checagem de review trigger). Carregar a skill e rodar o protocolo sao passos separados. Depois de concluir cada tarefa, reporte em 1 linha as observacoes registradas nesta sessao (ids e titulos, ou 'nenhuma registrada')."}}
JSON
exit 0
