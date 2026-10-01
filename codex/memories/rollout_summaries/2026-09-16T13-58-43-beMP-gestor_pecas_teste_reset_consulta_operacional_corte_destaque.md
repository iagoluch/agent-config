thread_id: 01a0aa83-4007-7f51-8b13-f9ffc65364c3
updated_at: 2026-09-16T14:58:16+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\16\rollout-2026-09-16T10-58-43-01a0aa83-4007-7f51-8b13-f9ffc65364c3.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes
git_branch: master

# TESTE resetado, Consulta Operacional reorganizada e Corte desacoplado do Destaque

Rollout context: Projeto Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, com PostgreSQL TESTE/REAL separados.

## Task 1: Limpeza controlada do banco TESTE

Outcome: success

Preference signals:
- O usuário pediu: “Exclua dados do banco teste, apenas op e informações relacionadas” -> preservar estrutura, usuários e cadastros; não tocar no REAL.

Key steps:
- Executado `scripts/resetar_banco_teste.py --dry-run` com confirmação de `gestor_pecas_test`.
- Dry-run confirmou TESTE `gestor_pecas_test`, REAL `gestor_pecas` somente leitura, schema 37 e 71.336 registros elegíveis.
- Executada limpeza transacional com `--confirmar gestor_pecas_test`.
- Foram removidos dados de OP, planejamento, execução, Corte, Qualidade, outbox e envelopes `ProductionOrder`; usuários, recursos, calendários, configurações, mensagens não-OP e schema foram preservados.
- Estado registrado em `docs/STATUS_ATUAL.md`.

Reusable knowledge:
- A rotina oficial exige confirmação literal do banco e valida TESTE/REAL, schema, contagens antes/depois e integridade pós-commit.
- O REAL é aberto em `default_transaction_read_only=on` e não sofre mutação.

## Task 2: Recursos sem demanda, nomes líquidos e organização por setor

Outcome: success

Preference signals:
- O usuário pediu que “Recurso sem demanda” apareça apenas para recursos vinculados às contas cadastradas e ativas -> não usar inventário inteiro, OP, rota ou demanda como critério.
- Pediu: “recursos que apareçam o nome bruto eu não quero, quero o nome liquido dele” e depois “com a primeira letra maiusculo obviamente” -> exibir descrição amigável com capitalização normal, mantendo código interno.
- Pediu abas/dropdown por setor para não deixar recursos misturados -> mostrar um setor por vez na Visão Geral.

Key steps:
- `FrontendBackendFacade.consulta_operacional` passou a projetar recursos sem demanda a partir de `usuarios` ativos e `OPERATOR_PROFILES`.
- Andon e Dev Observatory continuam restritos a apontamentos canônicos.
- Visão Geral ganhou seletor de setor e cards exibem apenas os recursos do setor escolhido.
- Recursos ganharam `recurso_nome`; a UI usa nomes líquidos como “Dispositivo exportação”, “Serviços gerais” e “Reforma dispositivos”.
- Build Web passou com sucesso; testes direcionados reportados como 16/16 e 21 testes de nomenclatura.
- API TESTE validada em `127.0.0.1:8001`, capabilities HTTP 200, `active_data_source=postgresql_test_only`.

Failures and how to do differently:
- Uma execução de `pytest` falhou porque `pytest` não está instalado no `.venv`; usar `unittest` direcionado neste ambiente.
- A suíte maior ficou presa no encerramento de teste e foi interrompida; não tratar isso como falha funcional sem reproduzir.

## Task 3: Conclusão de Corte independente do Destaque

Outcome: success

Preference signals:
- O usuário definiu que, após todos os nestings da OP serem finalizados, a etapa `CORTE` deve estar concluída; Destaque é apenas contabilização de tempo e não pode travar a OP.
- Também esclareceu que a associação deve respeitar OP + programa/nesting, sem uma OP bloquear outra do mesmo agrupamento.

Key steps:
- Criado `_corte_concluido_sql` em `app/database/database.py`.
- A conclusão é calculada por OP e programa/nesting, exigindo todos os planos correspondentes finalizados, sem exigir status do Destaque.
- `listar_roteiro_completo_op` e `listar_proximas_operacoes_roteiro` foram ajustados.
- Teste novo cobre duas OPs no mesmo agrupamento e confirma que somente a OP com seus nestings concluídos avança.
- Testes críticos passaram: 2/2, incluindo independência do Destaque e fluxo persistente do Destaque.
- Tudo foi commitado no commit `a8e29c0 fix: separar conclusao do corte do destaque`.

References:
- Limpeza: `scripts/resetar_banco_teste.py --dry-run`; `scripts/resetar_banco_teste.py --confirmar gestor_pecas_test`
- Consulta: `mes/services/frontend_facade.py`, `backend/api/routers/operations.py`
- UI: `web/src/pages/operations/OperationsPages.tsx`, `web/src/components/ResourceCard.tsx`, `web/src/utils/format.ts`
- Mapeamento: `app/core/resource_mapping.py`
- Corte: `app/database/database.py`, `tests/test_totvs_operator_queue.py`
- Commit final: `a8e29c0`
