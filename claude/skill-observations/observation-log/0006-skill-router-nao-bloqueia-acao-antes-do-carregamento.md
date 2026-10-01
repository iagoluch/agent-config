---
id: 6
title: "Skill router nao bloqueia acao antes do carregamento da skill relevante"
status: open
type: internal
skill: [skill-router]
proposes_skill: []
target_file: ["~/.codex/hooks.json"]
siblings_checked: "using-agent-skills e browser-testing-with-devtools avaliadas; falha pertence ao roteador do ambiente Codex, sem propagacao de conteudo"
area: "ativacao estrutural de skills antes da primeira ferramenta de dominio"
date: 2026-09-29
session_context: "Construcao de crawler do TOTVS no Codex Chrome; duas inspecoes do navegador ocorreram antes do carregamento de browser-testing-with-devtools, apesar do match semantico direto. Em 2026-10-01, a consolidacao de memoria tambem precisou localizar e ler task-observer por ferramenta antes de poder executar o Session Start Protocol, embora a instrucao exigisse isso antes da primeira ferramenta."
parked_until: ""
resolved: ""
resolution: ""
reference: ""
---

**Issue:** O fluxo iniciou inspecao real do navegador antes de carregar `browser-testing-with-devtools`. A skill foi reconhecida somente depois, mesmo com regra global de acionamento semantico e com a observacao #4 ja actioned para o ambiente Claude. Isso demonstra que o gatilho mecanico existente nao cobre o Codex Chrome e que a descricao/catalogo ainda permite a primeira ferramenta de dominio escapar. Em 2026-10-01, a consolidacao de memoria repetiu a falha de precondicao: foi necessária uma ferramenta para localizar e carregar `task-observer` antes de executar o protocolo que deveria preceder a primeira ferramenta.

**Suggested improvement:** Adicionar uma barreira estrutural no roteamento do Codex que, antes da primeira chamada de ferramenta de dominio, resolva skills semanticamente aplicaveis e carregue seus `SKILL.md`; para tarefas de navegador, a chamada deve ser recusada ou precedida automaticamente pelo carregamento da skill correspondente. Validar com controle positivo real (`cua` em tarefa browser) e negativo real (comando de filesystem sem tarefa browser).

**Principle:** Quando uma metodologia precisa valer antes da primeira acao, sua ativacao deve ser uma precondicao mecanica da ferramenta, nao uma lembranca baseada em descricao.
