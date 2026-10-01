"""SessionStart: avisa o Claude sobre memórias do OpenCode/Nemotron pendentes de revisão.

O plugin claude-compat.js do OpenCode grava memórias novas em
~/.claude/projects/<id>/memory/inbox/. Aqui o Claude é instruído a revisá-las
(promover ao MEMORY.md ou descartar) antes da tarefa do usuário.
"""
import json
import os
import re
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def project_cwd() -> str:
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except (ValueError, OSError):
        data = {}
    return data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def memory_dir(cwd: str) -> Path | None:
    project_id = re.sub(r"[^A-Za-z0-9]", "-", cwd)
    if not PROJECTS.is_dir():
        return None
    for entry in PROJECTS.iterdir():
        if entry.name.lower() == project_id.lower():
            return entry / "memory"
    return None


def description(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:12]:
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def main() -> None:
    mem = memory_dir(project_cwd())
    inbox = mem / "inbox" if mem else None
    if not inbox or not inbox.is_dir():
        return
    pending = sorted(p for p in inbox.glob("*.md") if p.is_file())
    if not pending:
        return
    items = "\n".join(f"- {p.name}: {description(p)}" for p in pending)
    context = (
        f"Caixa de entrada de memória: {len(pending)} memória(s) gravada(s) pelo OpenCode/Nemotron "
        f"aguardam revisão em {inbox}:\n{items}\n\n"
        "Antes da tarefa do usuário, revise cada uma: PROMOVER (mover para o diretório memory/, "
        "remover os campos source/created do frontmatter, mesclar com uma memória existente se "
        "for duplicada e adicionar a linha `- [Título](arquivo.md) — gancho` no MEMORY.md) ou "
        "DESCARTAR (errada, trivial ou já coberta: mover para inbox/_descartadas/, nunca apagar). "
        "Reporte o resultado em 1 linha e siga com o pedido do usuário."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


if __name__ == "__main__":
    main()
