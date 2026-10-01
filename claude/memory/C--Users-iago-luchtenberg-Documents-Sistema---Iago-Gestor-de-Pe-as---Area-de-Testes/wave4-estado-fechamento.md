---
name: wave4-estado-fechamento
description: Onde a Wave 4 parou em 2026-09-08 e o que falta para fechar e promover o banco REAL
metadata: 
  node_type: memory
  type: project
  originSessionId: fbd404ff-6e5c-4b24-9b6f-6e1f5f212a47
  modified: 2026-09-08T20:25:20.375Z
---

Wave 4 parada em 2026-09-08 a pedido do usuário. Estado detalhado em `outputs/wave4_visual/ESTADO_WAVE4.md`.

Verde: Web 80/80, build TS 389 módulos, migration 25 aplicada+validada SÓ em `gestor_pecas_test` (schema 25, CHECK `ck_apontamentos_quantidade_atendida_planejada` NOT VALID), cadeia de migrations 8/8. Banco REAL `gestor_pecas` intocado em schema 11.

Faltam 2 bloqueios (suíte Python completa: 689 testes, 13 falhas + 4 erros):
1. Bug real de produção: `database.py:4276` `listar_cortes_ativos_andon` seleciona `corte.sigmanest_repeat_id` de `apontamentos_corte`, coluna que só existe em `catalogo_sigmanest_planos_corte` → quebra Andon no PostgreSQL + viola guard arquitetural. Corrigir causa raiz.
2. ~15 testes/fixtures legados esperam `boas + refugo > planejado`. DECISÃO do usuário (2026-09-08): teto = planejado, `boas + refugo` nunca excede. CHECK da migration 25 e o ValueError em `operator_flow` estão certos; os testes é que devem ser atualizados.

Depois de 100% verde: backup `pg_dump` do REAL → validar restore → preflight 11→25 → OK final do usuário → promover `gestor_pecas` 11→25. Usuário já autorizou a promoção e disse ter credencial de escrita, mas só após o verde e o backup.

NÃO afrouxar a CHECK da migration 25. NÃO inventar datas SigmaNEST (T3528/T3539 e vínculo login↔estação de Solda seguem BLOQUEADO POR DADO). Ver [[etapa7-e2e-op-candidata]].
