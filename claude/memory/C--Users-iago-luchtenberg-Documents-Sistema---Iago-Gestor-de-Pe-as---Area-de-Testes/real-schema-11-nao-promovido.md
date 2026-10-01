---
name: real-schema-11-nao-promovido
description: "REAL (gestor_pecas) em v53 desde 30/09/2026 (m53 limpou histórico legado) e trava do 'test' no nome removida (5224c7f); ligar = GESTOR_WEB_ENV=production + GESTOR_EXPECTED_DATABASE=gestor_pecas"
metadata:
  node_type: memory
  type: project
  originSessionId: e0fd2345-b785-4137-ad84-99a6840ec7e9
  modified: 2026-09-30T12:00:28.949Z
---

Em 30/09/2026, com aprovação do usuário, o REAL `gestor_pecas` (Docker local, porta 15432) foi promovido de `schema_migrations` v11 para **v52**.
- Ensaio feito antes numa cópia.
- Contagens preservadas.
- BK-17 validada.
- Backup da v11: `dev_reports/backup_real/gestor_pecas_v11_20260930.dump`.

No mesmo dia, o usuário pediu para remover a trava de nome `test` em `Database.__init__` (commit `5224c7f`). O app já consegue abrir o REAL: a prova foi feita somente leitura, com schema 52 = app 52.

**Why:** o REAL ainda não estava em operação, então as travas de "só TEST" viraram atrito sem proteger nada.

**How to apply:**
- Para o app usar o REAL, trocar no `.env`:
  - `GESTOR_WEB_ENV=production`;
  - `GESTOR_EXPECTED_DATABASE=gestor_pecas`.
- Com isso, pytest nessa máquina passa a recusar o TEST por identidade (comportamento esperado).
- Continuam as guardas de `test` no nome dos scripts de seed/limpeza e do `simulation_mode`: não removê-las junto.
- Mudanças de schema futuras precisam ser aplicadas também no REAL.


30/09/2026 ~16h: REAL promovido a **v53** (migration 53, commit 87f1026): histórico de `eventos_estado_recurso` com nome legado (1303, Laser Ensis 3015…) convertido para o código canônico e CHECK `ck_eventos_estado_recurso_codigo_canonico` VALIDADA — é isso que impede o card de setor duplicado de voltar. Backup antes: `dev_reports/backup_real/gestor_pecas_v52_20260930_antes_m53.dump`. Se um alias mudar no futuro, criar migration NOVA; nunca editar a 53 (já aplicada).
