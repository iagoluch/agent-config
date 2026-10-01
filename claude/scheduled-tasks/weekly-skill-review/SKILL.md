---
name: weekly-skill-review
description: Revisão autônoma do observation-log do task-observer; aplica em staging, nunca instala.
---

Rode a revisão agendada do task-observer em modo AUTÔNOMO (usuário ausente). Responda em pt-BR.

1. Carregue a skill `task-observer` (Skill({skill:"task-observer"})) e então leia `C:\Users\iago.luchtenberg\.claude\skills\task-observer\references\weekly-review.md` e siga-o do Step 1 ao Step 8, no modo "Scheduled autonomous".
2. Workspace (caminho absoluto, sempre entre aspas; use bash explicitamente): `C:\Users\iago.luchtenberg\.claude\skill-observations` (em bash: `/c/Users/iago.luchtenberg/.claude/skill-observations`).
3. Política offline: antes de tudo faça `ls` do workspace. Se não existir/inacessível, encerre com uma linha "review skipped — workspace offline", sem retries. Falha de permissão no meio: pule o passo, registre como follow-up manual e ainda assim emita o relatório final.
4. Aplique somente itens não escalados; escale (sem aplicar) propostas de skill nova, remoções/reestruturações decididas pelo agente, itens com incerteza e conflitos. Nunca edite skills vivas: tudo vai para `skill-updates/<data>/<skill>/`, validado com `scripts/validate-skill-bundle.py --pack`, com entrada em `skill-updates/PENDING.md`.
5. Rode o reconciliation gate de `PENDING.md` (diff -rq staged vs. vivo) e liste itens "actioned, awaiting install".
6. Re-cheque as condições `parked_until:` das entradas parked.
7. Atualize `last-review-date.txt` só se a revisão de fato rodou. Não espere confirmação no Step 8.
8. Termine com o resumo do Step 8 em pt-BR.