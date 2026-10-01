---
name: f21-backup-rotacao-infra
description: "F21 (backup/DR) — RPO/retenção decididos 23/09/2026, mas automação de rotação/agendamento fica com a infra, não com código do Gestor de Peças"
metadata:
  type: project
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T19:01:51.215Z
---

Decisões de F21 (backup/DR) fechadas em 23/09/2026: RPO 8/8h, destino por
enquanto na própria VM, retenção recomendada de 21 backups em janela rolante
(7 dias × 3/dia — ver `docs/STATUS_ATUAL.md` §3 item 7). Restore drill já era
da infra desde antes.

Usuário confirmou explicitamente em 23/09/2026: a **automação da rotação/
agendamento dos backups também fica com a infra**, não deve ser implementada
em código no repositório do Gestor de Peças. Pediu para guardar isso "para
uma resposta posterior" — ou seja, ainda não decidiu os detalhes de como a
infra vai automatizar, só que não é responsabilidade deste código.

**Why:** evita eu propor de novo implementar um script/cron de rotação de
backup dentro do projeto — já foi perguntado e a resposta foi "infra
resolve".

**How to apply:** se o assunto de rotação/agendamento de backup voltar,
não propor implementação em Python/script do repo por padrão; perguntar
primeiro se a infra já decidiu algo, e só implementar aqui se o usuário
pedir explicitamente que passe a ser responsabilidade do código.
