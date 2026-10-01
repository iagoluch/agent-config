---
name: pacote-deploy-vm-30-09-2026
description: Pacote de primeira instalação + runner self-hosted na VM (deploy/), ensaiado na VM VirtualBox do notebook em 30/09/2026; fluxo completo em deploy/LEIA-ME.md
metadata:
  type: project
  originSessionId: e0fd2345-b785-4137-ad84-99a6840ec7e9
  modified: 2026-09-30T18:05:15.641Z
---

30/09/2026: `deploy/` (instalar_prerequisitos.ps1, instalar_vm.ps1, instalar_runner.ps1, nginx.conf, montar_pacote.py, LEIA-ME.md). Zip em `dev_reports/deploy_vm/gestor-pecas-deploy.zip` (fora do git, contém dump do REAL + segredos). Fluxo inteiro (instalação → runner → deploy por tag → rollback → pendências externas) documentado em `deploy/LEIA-ME.md` §1–8.

Ensaio na VM VirtualBox "Gestor-Pecas-VM" (Windows Server 2025 Eval, NAT, redirects 127.0.0.1:80/443/33389): schema 52, ready 200.

Gaps fechados na 2ª rodada: app em conta virtual `NT SERVICE\gestor-pecas` (RX no app, M em dados\ e dev_reports\); docs/tests/.claude etc. fora do servidor (robocopy /XD no instalador e no deploy_release.ps1 — /XD não apaga o que já está no destino); nginx.conf propagado pelo deploy.yml com rollback; runner em conta virtual com permissões mínimas (instalar_runner.ps1). 3ª rodada (revisor independente): nginx também em `NT SERVICE\nginx`; as 3 contas com `sc privs SeChangeNotifyPrivilege/SeCreateGlobalPrivilege` (sem SeImpersonate = sem "potato" → SYSTEM); reexecução do instalar_vm.ps1 não pede senha do postgres se o `.env` conecta (senha só aceita no formato 48 hex); .venv recriada a cada instalação.

Fechado 30/09 ~15h: commit 8c43ac0 + tag `v0.0.1-ensaio` (run 36754967761) — CI, build, runner `win-q22cbuv9f82` (NT SERVICE, só SeChangeNotify/SeCreateGlobal), pg_dump pré-deploy, /ready 200 schema 52, login renderiza via https://localhost (NAT). "nginx.conf atualizado" no 1º deploy = CRLF do zip vs LF do checkout, some no próximo. Próximo pedido do usuário: um `instalar.ps1` único (preflight + perguntas só do que falta + chama os 3 scripts + backup diário agendado + apaga C:\instalacao + checklist final); wizard gráfico descartado.

Repo `iagoluch/gestor-de-pecas`: ficou privado por horas em 30/09 e VOLTOU a público (decisão do usuário) porque a cota de Actions de repos privados da conta está esgotada ("recent account payments have failed or your spending limit..."). Mitigação do runner em repo público: fork PR approval = `all_external_contributors`.

**Why:** usuário quis ensaiar "literalmente como o real" para achar gaps antes do servidor definitivo.

**How to apply:** não reinvestigar gaps já resolvidos. Pendências só externas: IP do Protheus (SOAP CIDRS), caminho de rede dos desenhos (conta virtual acessa rede como VM$), certificado corporativo, Telegram desligado. Teclado virtual (keyboardputstring) transborda/atrasa com o notebook carregado: linhas curtas e esperar a fila esvaziar; `:` e `|` chegam corrompidos (usar variáveis/$env:SystemDrive); tela da VM apaga e o screenshot dá E_FAIL — um Shift (scancode 2a aa) acorda; usuário disse para não se preocupar com a CPU. No ensaio o postgres-senha.txt ficou em C:\instalacao, fora de $Pacote. Remontar o zip exige HEAD limpo. Ver [[real-schema-11-nao-promovido]].


30/09 ~16h30: `deploy/instalar.ps1` (caminho único) + `deploy/backup_diario.ps1` (tarefa SYSTEM diária 02:00 a partir de C:\gestor-backup, retenção 14 d, cópia externa opcional via copia-externa.txt) ensaiados na VM com tag `v0.0.3-ensaio` (b0757a0; a v0.0.2 falhou no bandit B608, falso positivo marcado com nosec). Resultado: backup de teste OK, ready 200, pacote e C:\instalacao apagados. Gap achado e corrigido (307f37d): remover C:\instalacao falhava com o console dentro dela. Pendências: pasta externa real do backup, alertas de falha, remover usuário `iagodev` (id 14) antes da produção, guardar C:\gestor-backup\postgres-senha.txt num cofre. Na VM: `curl` sem `http://` (o `:` antes de `/` cru deixa Shift preso no vmtype).
