thread_id: 01a0f688-3b41-77e1-bc2e-07f4e65068f3
updated_at: 2026-09-30T14:15:30+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\10\01\rollout-2026-10-01T05-15-18-01a0f688-3b41-77e1-bc2e-07f4e65068f3.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\AppData\Roaming\Claude\scratch-workspaces\3b9c2856-223a-4112-aa9a-9b9de00331d6\94900231-2415-49d7-9bb6-2ce48172cbea\scratch-2026-09-30-aed621

# Windows Sandbox harness criado e validado parcialmente

Rollout context: O usuário pediu, em português, um `.wsb` e scripts PowerShell para executar testes de projetos em um Windows Sandbox descartável. O trabalho ocorreu em uma pasta temporária da sessão.

## Task 1: Criar launcher e script guest para Windows Sandbox

Outcome: partial

Key steps:
- Criados `sandbox/launch.ps1` (host) e `sandbox/guest/run.ps1` (guest).
- O launcher sanitiza uma cópia do repositório, removendo `.git`, `node_modules`, `.venv`, `.env*`, `*.pem`, `*.key` e `*.pfx`.
- Gera um `runs/<timestamp>/run.wsb` com código somente leitura, scripts guest somente leitura e diretório de saída gravável.
- O guest executa setup/teste, registra `setup.log`, `test.log`, `guest.log` e grava `result.json` ao final.
- Adicionado BOM UTF-8 aos dois `.ps1` para compatibilidade com Windows PowerShell 5.1.
- O desligamento automático foi protegido para ocorrer apenas quando executado como `WDAGUtilityAccount`.

Reusable knowledge:
- O host tem hypervisor presente, mas a feature Windows Sandbox não estava instalada; `WindowsSandbox.exe`/`wsb.exe` não foram encontrados. A habilitação exige PowerShell elevado e reinicialização: `Enable-WindowsOptionalFeature -Online -FeatureName "Containers-DisposableClientVM" -All`.
- Ambos os scripts passaram na checagem de sintaxe.
- Dry-run confirmou a cópia sanitizada e a geração do XML `.wsb`; a cópia excluiu os arquivos sensíveis e diretórios esperados.
- O guest foi exercitado no host em seis cenários: exit code 3, sucesso com aspas/`&&`, stderr, timeout (`124`), setup bem-sucedido e setup falho (`98`).

Failures and how to do differently:
- A primeira simulação falhou porque o caminho de trabalho tinha mais de 260 caracteres; `cmd.exe` retornou “O nome do diretório é inválido”. Reexecutar com caminho curto resolveu o problema.
- Uma tentativa de limpar um diretório protegido foi bloqueada; usar um diretório temporário curto e específico evitou isso.
- O boot real do Sandbox, mapeamento das pastas e downloads de Python/Node não foram testados, portanto a solução ainda precisa de validação em uma máquina com a feature habilitada.

References:
- `sandbox/launch.ps1`
- `sandbox/guest/run.ps1`
- Comandos de uso: `.\sandbox\launch.ps1 -RepoPath "C:\caminho\do\projeto" -TestCommand "python -m pytest -q" -DryRun` e a mesma chamada sem `-DryRun`.
- Códigos reservados: `98` setup falhou, `99` erro interno do script, `124` timeout.
- Resultado validado: `exit=3`, `exit=0`, `exit=1`, `exit=124`, `setup=0`, `exit=98`.

