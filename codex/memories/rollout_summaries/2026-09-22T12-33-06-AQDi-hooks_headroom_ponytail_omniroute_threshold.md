thread_id: 01a0c91b-0782-77b2-b2a1-53debb3d6e74
updated_at: 2026-09-22T12:26:05+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\22\rollout-2026-09-22T09-33-06-01a0c91b-0782-77b2-b2a1-53debb3d6e74.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Auditoria e automação de skills, MCPs e hooks no projeto Gestor de Peças

Rollout context: Projeto em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, com Claude Code/Claude Desktop, hooks locais, MCPs e git hooks.

## Task 1: Auditar uso de skills, plugins, MCPs e hooks

Outcome: success

Key steps:
- Confirmado que `graphify` é usado ativamente e imposto por `PreToolUse` (`graphify hook-guard search/read`).
- Confirmados hooks de TypeScript, git `post-commit` e `post-checkout`, incluindo rebuild automático do graphify.
- Plugins instalados: `pg@aiguide` e `claude-code-setup`; `pg-aiguide` é condicional a tarefas PostgreSQL.
- `context7`, Playwright, Schemathesis e ferramentas de segurança já estavam documentados como adotados; várias skills Office/SaaS permanecem inativas por falta de gatilho.
- `omniroute`, `headroom` e `pg-aiguide` estavam conectados, mas não necessariamente utilizados em toda sessão.

Reusable knowledge:
- Para descobrir MCPs user-registered, `claude mcp list`/`get` é mais confiável que procurar chaves em `.claude.json`.
- `headroom` depende do proxy local em `127.0.0.1:8787`; sem ele, `headroom_compress` retorna `router:noop`.

## Task 2: Remover omniroute e tornar headroom utilizável

Outcome: success

Preference signals:
- O usuário pediu explicitamente: “desativa o omniroute” e que o headroom fosse tornado utilizável ou substituído -> futuras mudanças devem remover ferramentas não usadas e buscar uso real antes de mantê-las.
- O usuário preferiu automação persistente em vez de depender apenas de memória/instrução manual.

Key steps:
- `claude mcp remove omniroute` removeu o servidor com sucesso.
- Removidos o `SessionStart` órfão e `.claude/hooks/omniroute-autostart.sh`.
- Criado `headroom-autostart.sh` para iniciar o proxy local com `nohup`, de modo best-effort.
- Teste estruturado comprimiu 542 para 389 tokens, economia de 28,2%; saída mista de git/graphify resultou legitimamente em `router:noop`.
- Limitação validada: Claude Desktop não roteia o tráfego da própria conversa pelo proxy; uso manual via MCP continua possível.
- Commit/push: `2a3edd0`.

Failures and how to do differently:
- Backgroundar com `& disown` foi inconsistente; `nohup ... > /tmp/log 2>&1 & disown` deixou o proxy persistente e verificável.
- Não assumir que MCP “connected” significa compressão ativa; verificar o proxy e `headroom_stats`.

## Task 3: Criar enforcement real para ponytail e headroom

Outcome: success

Key steps:
- Criado `ponytail-reminder.sh` em `UserPromptSubmit`, injetando lembrete para tarefas de código.
- Criado `headroom-remind.sh` em `PostToolUse` para `Bash|Grep`; inicialmente bloqueava acima de 3000 bytes.
- Teste de saída grande disparou bloqueio real via `{"decision":"block"}`.
- Threshold ajustado para 12000 bytes para evitar ruído em saídas moderadas; teste de ~4 KB passou e saída de ~31,7 KB disparou o hook.
- Commit/push dos hooks: `ced1bf2`; ajuste do threshold: `0abf423`.
- Memórias de ponytail/headroom foram atualizadas para refletir enforcement técnico.

Preference signals:
- O usuário pediu: “cria o hook de verdade pros dois” -> quando pedir garantia de execução, prefere hooks mecânicos, não apenas memória ou disciplina do agente.
- O usuário pediu economia sem deixar o agente “burro” -> thresholds devem privilegiar evitar falsos positivos e preservar contexto útil.
- O usuário questionou o custo de “60 tokens a cada mensagem” fora de coding -> há preocupação explícita com overhead fixo e lembretes irrelevantes; não tratar como decisão final para filtrar, pois nenhuma implementação de filtro foi aprovada.

Reusable knowledge:
- `UserPromptSubmit` é adequado para lembrete por mensagem; `PostToolUse` é adequado para compressão porque a saída só existe depois da ferramenta.
- 12000 bytes (~3000 tokens) foi o threshold validado empiricamente como filtro razoável: não bloqueou ~4 KB e bloqueou ~31,7 KB.
- O hook de headroom sinaliza compressão, mas não garante economia: o router pode retornar `router:noop`.

Failures and how to do differently:
- O hook de ponytail injeta texto em toda mensagem, inclusive não-coding, gerando custo fixo estimado de ~60 tokens; o último estado do rollout ainda não implementou filtro semântico/por palavras-chave.
- Não afirmar que os hooks economizam tokens diretamente: ponytail tem custo de contexto e benefício indireto; headroom só economiza quando classifica conteúdo como compressível.

References:
- `.claude/settings.json`
- `.claude/hooks/ponytail-reminder.sh`
- `.claude/hooks/headroom-remind.sh`
- `.claude/hooks/headroom-autostart.sh`
- Commits `2a3edd0`, `ced1bf2`, `0abf423`
- Erro/limitação: `Desktop routing is not supported yet (see #869)`

## Task 4: Decidir se o lembrete ponytail deve ser filtrado fora de coding

Outcome: uncertain

Key steps:
- A skill `ponytail` declara explicitamente: usar em coding e não usar em conhecimento geral, prosa, tradução ou resumos.
- O hook atual sempre dispara, mas inclui instrução para ignorar em prompts não relacionados a código.
- O usuário apontou que o custo fixo pode ser desnecessário; o assistente sugeriu filtro heurístico, mas o usuário não aprovou nem rejeitou a mudança.

Failures and how to do differently:
- Próxima ação deve tratar filtro condicional como decisão pendente, não como preferência consolidada. Se implementado, validar falsos negativos em tarefas de código sem palavras-chave óbvias.
