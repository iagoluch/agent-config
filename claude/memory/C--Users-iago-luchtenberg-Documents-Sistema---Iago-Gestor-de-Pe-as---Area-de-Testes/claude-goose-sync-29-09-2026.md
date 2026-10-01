---
name: claude-goose-sync-29-09-2026
description: "Camada de sync contínuo Claude Code → Goose 1.52 + Nemotron 3 Ultra, em ~/.claude-goose-sync; 8 validações passaram em 29/09/2026."
metadata:
  node_type: memory
  type: project
  originSessionId: 6ec46f4d-d3d4-4db7-bead-448e103dba7f
  modified: 2026-09-29T13:02:51.569Z
---

Goose + Nemotron espelham o ambiente do Claude via `~/.claude-goose-sync/claude_goose_sync.py`
(sync/watch/status/rollback/install-autostart) + `hook_bridge.py`. Watcher sobe no login
(Startup\claude-goose-sync.vbs → pythonw) e também em todo SessionStart do Goose.

Gotchas já resolvidos — não reinvestigar:
- Goose roda hooks com `sh -c` até no Windows → Git\bin foi acrescentado ao PATH do usuário (registro).
- Stdout de hook do Goose não entra no contexto do modelo → notas vão para o Top of Mind
  (`GOOSE_MOIM_MESSAGE_FILE` = out/top_of_mind.md; Desktop precisa reiniciar para ler).
- `~/.claude/skills` é lido nativamente, mas `~/.agents/skills` vence; 9 skills lá são
  adaptações do Codex (drift reportado, nunca sobrescrito).
- pythonw tem stdout None → guard no `__main__`.
- Shell do Goose no Windows é cmd: sem `find -name`/`rg`.

**Why:** o usuário usa Nemotron para poupar Claude; o Claude segue fonte de verdade e livre.
**How to apply:** ao mudar CLAUDE.md, skills, MCPs, hooks, agentes ou memória, não é preciso
fazer nada no Goose; conferir `python ~/.claude-goose-sync/claude_goose_sync.py status` se algo
não aparecer. Memória vinda do Goose chega por `memory/inbox/` (source: goose-nemotron).

**Trava de concorrência (29/09/2026, 11:19):** `cmd_sync` roda dentro de `sync_lock()` (msvcrt em `state/sync.lock`). Antes, watcher + sync manual simultâneos causavam conflito fantasma no manifest e WinError 32 no `.cgs-tmp`. Prova: 4 syncs simultâneos sem erro; sync concorrente espera (4,0s vs 0,6s). Após editar o script, **reiniciar o watcher** (ele mantém o código antigo em memória): matar o pid de `state/watch.pid` e rodar o `.vbs` do Startup. Backup: `backups/claude_goose_sync.py.pre-lock-20260929`.

**Teste ponta a ponta 29/09/2026 (tarde):** Goose CLI (`resources\bin\goose.exe run`) enxerga extensões, skills (load_skill ok), 26 agentes, regras do .goosehints e **delega subagente** (`delegate` → qa-test-engineer, ok). MAS no CLI os hooks do plugin claude-sync NÃO disparam (nem SessionStart: sync.log sem `goose-session-start`, hook_notes sem a sessão) e o Top of Mind não chega ao modelo. No **Goose Desktop** disparam (sessão 20260929_5 gravou SessionStart+UserPromptSubmit). Não é bug do sync — não "corrigir" o bridge por causa do CLI. Para testar CLI no PowerShell 5.1, passe o prompt via stdin (`$p | goose run -i -`): aspas duplas em `-t` quebram o argumento.

**Regra máxima do Goose (29/09/2026):** fonte em `~/.claude-goose-sync/goose_rules.md` (só Goose, não afeta o Claude); o sync injeta no `.goosehints` global logo após o preâmbulo + 1 linha-resumo no topo do Top of Mind; watcher monitora o arquivo. Cita skills Superpowers (`systematic-debugging`, `verification-before-completion`) que NÃO estão instaladas — nota operacional manda aplicar as LEIs direto. Mesmo dia: corrigido ping-pong do `hooks.json` do plugin (intérprete derivado de quem rodava o sync: python vs pythonw e 2 instalações) — agora fixo `C:/Python314/pythonw.exe` via `python_exe(windowed=True)`. Backups `*.pre-regra-critica-20260929`.

**Superpowers (29/09/2026, opção 2 escolhida pelo usuário):** plugin `superpowers@claude-plugins-official` v6.3.0 (sha b36e082) instalado no Claude (user scope, 14 skills + hook SessionStart que injeta `using-superpowers`). O sync espelha 14 skills em `~/.agents/plugins/claude-superpowers/skills` e o hook via hook_bridge; Goose CLI carregou `systematic-debugging` e `verification-before-completion` com `load_skill`. 2 bugs do sync corrigidos: (1) hook_bridge não exportava `CLAUDE_PLUGIN_ROOT` → hook de plugin falhava calado (agora spec leva `plugin_root`); (2) skill de plugin homônima sobrescrevia em silêncio o espelho `~/.agents/skills/<nome>` (caso `test-driven-development`) → agora a 1ª fonte (~/.claude/skills) é dona e a homônima fica sombreada e reportada em "Ignorados". Backups `*.pre-superpowers-20260929` em `~/.claude-goose-sync/backups/`. Desinstalar = `claude plugin uninstall superpowers@claude-plugins-official` + sync. `claude -p` no terminal não está logado (Desktop tem login próprio) — não serve para testar o Claude.
