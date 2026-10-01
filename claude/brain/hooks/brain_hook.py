import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone

for _stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HOME = Path(os.environ.get("USERPROFILE") or Path.home())
CLAUDE = HOME / ".claude"
BRAIN = CLAUDE / "brain"
STATE = BRAIN / "state" / "current.md"
LOG = BRAIN / "logs" / "activity.log"

def read_stdin():
    try:
        raw = sys.stdin.buffer.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}

def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def run_cmd(args, cwd=None):
    try:
        p = subprocess.run(
            args, cwd=cwd, capture_output=True, timeout=8,
            encoding="utf-8", errors="replace",
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception:
        return 1, "", ""

def git_state(cwd):
    code, branch, _ = run_cmd(["git", "branch", "--show-current"], cwd)
    code2, status, _ = run_cmd(["git", "status", "--porcelain"], cwd)
    if code != 0:
        branch = "não é um repositório Git"
    if code2 != 0:
        status = ""
    changed = []
    for line in status.splitlines():
        if len(line) >= 4:
            changed.append(line[3:])
    return branch or "detached/sem branch", changed[:20]

def project_name(cwd):
    p = Path(cwd)
    return p.name or str(p)

def update_state(data, reason):
    cwd = data.get("cwd") or os.getcwd()
    branch, changed = git_state(cwd)
    timestamp = now()
    current = f"""# Estado atual

## Sessão
- Última atividade: {timestamp}
- Motivo da atualização: {reason}
- Diretório atual: `{cwd}`
- Projeto: `{project_name(cwd)}`
- Branch: `{branch}`

## Alterações Git detectadas
"""
    if changed:
        current += "\n".join(f"- `{x}`" for x in changed)
    else:
        current += "- Nenhuma alteração detectada ou Git indisponível."

    current += """

## Próximo passo
- Determinar pelo pedido atual do usuário; não presumir.
"""
    STATE.write_text(current, encoding="utf-8")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp}\t{reason}\t{cwd}\t{branch}\t{len(changed)} arquivos alterados\n")

def memory_context(data):
    cwd = data.get("cwd") or os.getcwd()
    parts = []
    for p in [
        BRAIN / "context" / "user.md",
        BRAIN / "context" / "rules.md",
        BRAIN / "state" / "current.md",
    ]:
        if p.exists():
            text = p.read_text(encoding="utf-8").strip()
            if text:
                parts.append(text)

    # Include the project memory only when it matches the current folder name
    name = project_name(cwd).lower()
    projdir = BRAIN / "projects"
    if projdir.exists():
        for p in projdir.glob("*.md"):
            if p.name.lower().replace("-", "_").startswith(name.replace("-", "_")[:12]):
                txt = p.read_text(encoding="utf-8").strip()
                if txt:
                    parts.append(txt)

    ctx = "\n\n---\n\n".join(parts)
    # Keep SessionStart context comfortably below the Claude hook cap.
    return ctx[:8500]

def main():
    event = sys.argv[1] if len(sys.argv) > 1 else "noop"
    data = read_stdin()
    if event in ("session-start", "prompt", "stop", "session-end", "tool"):
        update_state(data, event)

    if event in ("session-start", "prompt"):
        ctx = memory_context(data)
        if event == "session-start":
            # Plain stdout on SessionStart is injected into Claude's context.
            print("CLAUDE BRAIN — CONTEXTO AUTOMÁTICO")
            print(ctx)
        else:
            # UserPromptSubmit also injects plain stdout into context.
            print("BRAIN CONTEXT")
            print(ctx)

if __name__ == "__main__":
    main()
