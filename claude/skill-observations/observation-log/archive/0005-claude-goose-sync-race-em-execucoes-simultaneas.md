---
id: 5
title: "claude-goose-sync corrompe manifest/canonical quando watcher e sync manual rodam juntos"
status: actioned
type: improve-skill
skill: []
proposes_skill: 
target_file: ["~/.claude-goose-sync/claude_goose_sync.py"]
siblings_checked: "nenhuma observação prévia sobre o sync"
area: "sync Claude -> Goose/Nemotron"
date: 2026-09-29
session_context: "Aplicando lote de mudanças no CLAUDE.md global; sync manual colidiu com o watcher (a cada ~5s)"
resolved: 2026-09-29
resolution: "sync_lock() com msvcrt em volta de cmd_sync; 4 syncs simultâneos sem erro; sync concorrente espera a trava (4,0s vs 0,6s); watcher reiniciado; backup em backups/claude_goose_sync.py.pre-lock-20260929"
reference: "memory/claude-goose-sync-29-09-2026.md"
---

Duas manifestações no mesmo dia: (1) conflito fantasma no hooks.json do Goose (registro antigo gravado por cima do novo por duas execuções concorrentes às 10:12), (2) PermissionError [WinError 32] no rename do canonical/*.json.cgs-tmp quando o sync manual rodou junto com o watcher. Ambos transitórios (reexecutar resolveu), mas o (1) passou horas silencioso e bloqueou a propagação de hooks novos.

Correção provável: lock de arquivo único (ex.: um .lock com fcntl/msvcrt ou um os.O_EXCL) no início de cmd_sync, para o watcher e o sync manual não escreverem manifest/canonical ao mesmo tempo. Não implementado ainda (usuário ainda alinhando o Goose; fora do escopo do lote de hoje).
