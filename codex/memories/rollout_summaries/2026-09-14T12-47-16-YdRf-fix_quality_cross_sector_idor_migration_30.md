thread_id: 01a09ff5-1dcb-7d10-b4ae-1aacf30efb69
updated_at: 2026-09-14T03:23:02+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-16-01a09ff5-1dcb-7d10-b4ae-1aacf30efb69.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Cross-sector IDOR in Quality inspections was fixed with persisted sector ownership and regression coverage

Rollout context: In `\\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, the user reported security finding M1: Quality write/read paths trusted an `inspecao_id` without rechecking the inspection's origin sector. The requested fix required a database migration, persistence of the origin sector when opening/dismissing inspections, a shared service guard, regression tests, and strict avoidance of the real `gestor_pecas` database.

## Task 1: Fix cross-sector IDOR in Quality inspection paths

Outcome: success

Preference signals:

- The user explicitly required: "Never touch the REAL database (gestor_pecas). Run at minimum ... plus add a regression test" -> future security fixes in this project should validate against disposable/test PostgreSQL and include an exploit-regression test before considering the work complete.
- The user specified that legacy rows without an origin sector must "stay visible to every sector, exactly like `_pertence_ao_setor` already does today" -> compatibility behavior for legacy data is an acceptance criterion, not an optional tightening.
- The user requested "One private helper on the service ... called at the top of `registrar_peca`, `finalizar_inspecao` and `obter_inspecao`. Single source of truth" -> similar authorization fixes should centralize the resource-boundary check and apply it consistently to read and write paths.
- The user warned that the existing TOTVS mapper failure was pre-existing and unrelated -> future validation should distinguish known baseline failures from regressions rather than treating every unrelated failure as caused by the patch.

Key steps:

- Added migration 30 in `app/database/migrations.py` to add nullable `qualidade_inspecoes.tipo_setor_origem` and backfill historical ownership from `catalogo_operacoes_op`; updated `SCHEMA_VERSION` from 29 to 30.
- Updated `app/database/quality_repository.py` and Quality service opening/dismissal flows to persist `tipo_setor_origem`.
- Changed repository derivation to prefer the persisted, nonblank column and only derive ownership as fallback for legacy rows, keeping history/summary queries consistent with authorization.
- Added `QualityInspectionService._exigir_setor(sessao)` using `quality_sector_for_user_level` and the existing sector rule; invoked it at the top of `registrar_peca`, `finalizar_inspecao`, and `obter_inspecao`.
- For `obter_inspecao`, cross-sector access returns `None` so the router preserves a 404-like non-disclosure behavior; write paths return service failure code `qualidade_inspecao_outro_setor`.
- Added tests covering refusal across all three paths and continued visibility of legacy inspections without ownership data.
- Updated `docs/AUDITORIA_SEGURANCA_2026-09-14.md` from DOCUMENTADO to CORRIGIDO.

Failures and how to do differently:

- The real production database was intentionally not modified. Applying migration 30 remains a deployment decision requiring a maintenance window; it performs an additive nullable column plus historical update.
- No git repository exists, so rollback is manual rather than a revert. The reported manual rollback would drop `tipo_setor_origem` and restore the schema version, but should be planned carefully before deployment.
- Sector denial currently maps to HTTP 409 because the router maps service failures to 409, matching the existing `qualidade_op_outro_setor` contract. Changing to 403 would require an explicit router contract change rather than an incidental alteration.

Reusable knowledge:

- The authorization bug existed because `qualidade_inspecoes.tipo_setor` stores the Quality appointment sector, not the originating production sector; deriving ownership from the current eligible-operation queue is unsafe because opening an inspection can remove the OP from that queue.
- Persisting the originating sector at inspection creation is the durable fix. The nullable column and fallback behavior preserve access to legacy records while preventing new cross-sector access.
- Repository consumers such as `listar_historico_qualidade` and `resumo_qualidade` must use the same persisted-first ownership logic as authorization to avoid inconsistent displays and enforcement.
- Validation reported 85 passing tests across `tests.test_quality_inspection`, `tests.test_permissions`, and `tests.test_web_api`, plus 80 passing migration/database/related-consumer tests. PostgreSQL integration exercised the migration and inserts in a disposable schema, and a directed smoke test exercised history/summary SQL with and without origin-sector data.

References:

- Primary worktree: `\\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`
- Files: `app/database/migrations.py`, `app/database/schema.py`, `app/database/quality_repository.py`, `mes/services/quality.py`, `tests/fakes.py`, `tests/test_quality_inspection.py`, `docs/AUDITORIA_SEGURANCA_2026-09-14.md`
- New schema artifact: `MIGRATIONS[30]`, `qualidade_inspecoes.tipo_setor_origem TEXT`, nullable
- Guard/error handle: `QualityInspectionService._exigir_setor`, `qualidade_inspecao_outro_setor`
- Reported validation groups: `tests.test_quality_inspection tests.test_permissions tests.test_web_api`; `tests.test_migration_chain_11_19 tests.test_database_professionalization tests.test_wave3_fluxo_apontamento tests.test_totvs_operator_queue`
- Known unrelated baseline failure: `tests.test_totvs_integration.TotvsParserContractTests.test_mapper_nao_inventa_setor_e_aplica_alias_laser_oficial_exato`
