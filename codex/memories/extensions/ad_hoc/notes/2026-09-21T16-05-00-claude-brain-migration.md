# Migração de memória operacional do Claude

Fonte conferida em `C:\Users\iago.luchtenberg\.claude\brain` em 21/09/2026.

- [FATO] O Brain classifica informações como FATO, DECISÃO, HIPÓTESE, PENDENTE e INFERÊNCIA; hipóteses e inferências não devem ser registradas como fatos.
- [FATO] Registre apenas informação durável: arquitetura, decisão, padrão, problema recorrente, mudança relevante, bloqueio ou próximo passo. Não registrar detalhes banais de sessão.
- [FATO] Preferências estáveis: priorizar Python/FastAPI e React/TypeScript quando forem o stack do projeto; usar Git/GitHub; preferir soluções simples e diretamente aplicáveis; evitar análise global e suíte completa quando a tarefa for localizada; validar de modo direcionado e proporcional.
- [FATO] Neste projeto, a integração Protheus/AdvPL vive em repositório separado; não inserir regras CP-1252/RDMake/AdvPL no repositório Python.
- [FATO] Estado de 21/09/2026: os commits `f838f66`, `282b305` e `bf34f2f` foram publicados no master. Permanecem WIP `scripts/resetar_banco_teste.py`, `scripts/clean-junk.ps1` e `scripts/register-clean-junk-task.ps1`.
- [PENDENTE] Não commitar o reset com preservação de OPs antes de corrigir a dupla subtração na contagem e adicionar cobertura. Não ativar a limpeza agendada antes de ela respeitar a quarentena e o nome de tarefa existente.

## Inventário de capacidade migrada

- [FATO] As 899 skills globais do Claude existem em `C:\Users\iago.luchtenberg\.agents\skills`; em 21/09/2026 as 47 que divergiam foram sincronizadas por hash. As cinco skills extras `source-command-*` são as equivalências dos comandos Claude `contexto`, `decidir`, `dia`, `fim` e `status`.
- [FATO] O plugin Claude Code Setup já estava ativo no Codex e sua skill é idêntica à do Claude. O PostgreSQL AI Guide foi trazido como MCP remoto `pg_aiguide` e suas nove skills locais foram migradas.
- [FATO] Headroom e OmniRoute já estavam configurados como MCPs no Codex. Os hooks globais de início de sessão e envio de prompt já chamam o Brain compartilhado; os hooks de Graphify, type-check TypeScript e autostart OmniRoute já existem no projeto.
