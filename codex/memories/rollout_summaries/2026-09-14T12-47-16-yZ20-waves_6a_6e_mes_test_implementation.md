thread_id: 01a09ff5-1ed5-7413-af41-5ce8c323df30
updated_at: 2026-09-13T01:45:15+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-16-01a09ff5-1ed5-7413-af41-5ce8c323df30.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Waves 6A–6E implemented in TEST, with one non-blocking business dependency remaining

Rollout context: The user directed a sequence of narrowly scoped MES waves in `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, explicitly requiring minimal-surface changes, preservation of existing engines/integrations, TEST-only work, no REAL/TOTVS/SigmaNEST production changes, directed tests before regression, and reporting of unresolved business ambiguities instead of inventing behavior.

## Task 1: Wave 6A — calendar, overtime, downtime, availability and OEE

Outcome: success

Preference signals:
- The user explicitly restricted implementation to Wave 6A and repeatedly required “não fazer refatoração geral”, reuse of existing calendar/OEE/state-machine services, and no REAL/TOTVS/SigmaNEST changes -> future work should audit current implementations and change the smallest possible surface.
- The user defined that the clock must never block an operator, planned overtime is a contextual calendar window, planned downtime must not affect OEE, and global out-of-shift time must not be duplicated by sector -> preserve these as acceptance criteria for temporal/OEE work.

Key steps:
- Added/reused calendar concepts for normal shift `08:00–17:30`, out-of-shift complement, and planned overtime using the existing `excecoes_calendario_produtivo.disponivel_extra` infrastructure.
- Made appointment permission unconditional by contract (`ManufacturingRules.appointment_allowed_at` always true); did not create a second calendar/OEE engine.
- Centralized stop classification into `PLANEJADA` / `NÃO_PLANEJADA`, with color derived centrally. “Sem apontamento” and “Recurso s/op” are unplanned.
- Changed global out-of-shift aggregation to temporal union while preserving resource/sector attribution.
- Corrected OEE inputs rather than rewriting the OEE formula; planned downtime no longer reduces availability.
- Removed the noisy physical-state alert from presentation while preserving internal diagnostics.
- Classified all 84 TEST catalog rows: 22 planned (group `0002 — PARADA PROGRAMADA`) and 62 unplanned; used guarded script `scripts/preencher_planejado_catalogo_status.py` requiring TEST database confirmation.

Reusable knowledge:
- Planned overtime remains a punctual window, not a permanent second shift. Existing `ShiftBoundaryService` still cuts at 17:30; the user confirmed operators should manually resume during overtime, matching the old MES.
- Planned classification is currently driven by the catalog’s `planejado` column, with group `0002` as the established criterion. REAL was not touched.
- Validated results included removal of roughly 11x global out-of-shift duplication and availability changing from roughly 76.2% to 96.2% in the tested period.

References:
- New tests: `tests/test_wave6a_calendario_operacional.py` (25 tests).
- Guarded catalog script: `scripts/preencher_planejado_catalogo_status.py`.
- Validation reported 290 Python regression tests, 33 Vitest tests and clean TypeScript build at the time.

## Task 2: Wave 6B — Setup/Quality gate and operator flow

Outcome: success

Preference signals:
- The user corrected the workflow several times and ultimately specified: Iniciar is free; the first piece is produced normally; Finalizar without Setup is blocked with guidance; clicking Setup records setup and opens the checklist; conformity releases the lot and automatically resumes production; subsequent production uses the normal single-start/single-finalize batch flow, not piece-by-piece like Corte.
- The user explicitly asked to remove the operator-facing Quality tab and separate First Piece card, but later corrected that the Setup button must remain as a real setup-time state. Future UI changes should distinguish presentation removal from domain/state removal.
- The user confirmed the dimensional `INSPECAO` flow is temporarily out of the operator process but must remain untouched in backend/domain/services.
- The user accepted automatic resumption being audited as the canonical ordinary `Retornar` event rather than introducing a new event type.

Key steps:
- Structured gate limited to Dobra, Usinagem and Serra; Solda, Pintura and Corte remain outside it.
- Removed the operator-facing Quality tab and separate First Piece card while retaining FirstPieceService/QualityService and existing quality inspection backend.
- Restored Setup as the sole source of `setup_registrado_em`; clicking Setup opens the existing checklist popup.
- Finalizar before Setup/first-piece approval is rejected with a human message; after Setup, the popup records measurements using existing Decimal tolerance logic (`referencia ± margem`).
- Conforming first piece releases the lot and triggers the canonical `Retornar` transition automatically; subsequent lot production remains one normal Iniciar and one normal Finalizar with quantities.
- Nonconformity preserves retrabalho/refugo flows and requires responsible authorization by badge for both retrabalho and refugo, with audit records.
- Added management history under Análises → Qualidade for first-piece/setup measurements and badge authorizations.
- Removed obsolete simulation packages/scripts because the user explicitly asked to delete them and revisit simulation later.

Reusable knowledge:
- The gate is enforced by backend/domain contracts, not just frontend visibility. Idempotency and concurrency protections were added/validated for start, checklist submission and finalization.
- Refugo is authorized before discard rather than represented as an OP block because database constraint `ck_primeira_peca_bloqueio` only permits active blocking in `RETRABALHO`; quantity/saldo semantics remain unchanged.
- The dimensional INSPECAO backend and `/quality/*` endpoints remain intact; only the operator entry point is absent by deliberate business decision.

Failures and how to do differently:
- Initial implementation incorrectly moved the quality gate to Iniciar and removed Setup; user corrections required restoring Setup and moving the gate to Finalizar→Setup. Future agents should confirm the exact operator sequence before editing UI/state transitions.

References:
- Main frontend: `web/src/pages/operator/WorkbenchPage.tsx`, `OperatorPortalPage.tsx`.
- New/updated tests: `tests/test_wave6b_gate_setup_qualidade.py` (final report: 35 tests), frontend reached 87/87 with clean `tsc -b` and build.
- Final validated sequence: `Iniciar` → produce first piece → `Finalizar` rejected if no Setup → `Setup` records state and opens checklist → conforming checklist → automatic `Retornar` → normal batch production.

## Task 3: Wave 6C — Corte hierarchy and Destaque read model

Outcome: success

Preference signals:
- The user required a minimal read-model/UX change, preserving SigmaNEST and canonical Destaque rules, with no invented OP/plan/nesting entities or quantities -> future agents should preserve source semantics and avoid inferring missing relationships.

Key steps:
- Changed Corte presentation to `Tarefa → Plano/Nesting → OP → Produto`, with expand/collapse and plan-level states.
- Preserved real SigmaNEST program/plan, sheet and repetition data; fixed the discarded `ProgramName` projection by adding nullable `programa` to the TEST catalog through migration 28.
- Kept Destaque availability on existing canonical `ManufacturingRules.cut_releases_highlight` / queue logic.
- Added plan-aware selection without creating a new operator flow.

Reusable knowledge:
- Legacy rows without program are deliberately shown as `OPs sem plano identificado` until the next SigmaNEST synchronization; do not guess assignment.
- Existing automatic nesting advancement may move to the next operational plan rather than current plan; this was explicitly left unchanged and is not a current blocker.

References:
- Frontend: `web/src/pages/operator/CuttingPage.tsx`.
- Tests: `tests/test_wave6c_hierarquia_corte.py` (24 tests), `web/src/test/cutting-hierarchy.test.tsx` (9 tests).
- Reported validation: 340 backend tests with only the then-known comment test failure, 96/96 frontend, clean build, visual two-plan/multiple-OP validation.

## Task 4: Wave 6D — Solda management and Andon TV

Outcome: success (implemented after an initial evidence-based stop)

Preference signals:
- The user initially accepted a likely custom field `B1_ZMODELO`, asked to implement the screen even before automatic ingestion exists, and accepted “Modelo não identificado.” until real values arrive.
- The user clarified that Solda stations should use actual observed OP pointing data, not an invented model/machine-to-station mapping.
- The user preferred proceeding with a defensible partial implementation rather than blocking the entire wave on unavailable ERP metadata.

Key steps:
- Initial agent correctly stopped before implementation when no evidence supported the requested `MODELO MAQUI` mapping or deterministic station mapping.
- After user clarification, implemented read-only Solda management endpoint/UI grouped by observed station, with OP/product/machine/date/status and nullable model.
- Added `catalogo_pcp_ops.produto_modelo` via TEST migration 29 but intentionally performed no ERP ingestion or load.
- Added Andon-only 10-second TV rotation between `/andon` and `/welding-management`; ordinary managers are not rotated.
- Used actual `apontamentos_operacionais.maquina` for stations; missing observations show a human “Estação ainda não definida.”
- Preserved Andon and integration behavior.

Reusable knowledge:
- The current TOTVS ProductionOrder ingestion does not populate `data_emissao` or `prazo_entrega`; only planned/release dates are available. Solda status uses `fim_planejado` as a declared partial basis, and no data means unavailable rather than inventing “A VENCER”.
- Automatic ingestion of `B1_ZMODELO` remains a future task; current UI displays “Modelo não identificado.” when null.

References:
- New backend: `mes/domain/welding.py`, `mes/services/welding.py`, `app/database/welding_repository.py`, `backend/api/routers/welding.py`.
- New UI: `web/src/pages/WeldingManagementPage.tsx`, `web/src/hooks/useTvRotation.ts`.
- Validation: 32 backend tests, 18 frontend tests, 149 web suite green, clean TypeScript/build, TEST visual validation with multiple stations/statuses.

## Task 5: Wave 6E — pause/badge filters and humanized presentation

Outcome: success

Preference signals:
- The user decided badges remain global; do not add a sector filter or sector field without a new business decision.
- The user wanted backend/AI mechanisms preserved while technical identifiers are humanized only at presentation boundaries.

Key steps:
- Added local persistent filters for Pausas and Crachás without new queries or endpoint/body changes.
- Centralized system-state humanization and applied it across management, production, reports, analytics, audit and AI presentation.
- Preserved provider, streaming, tool calling and AI persistence mechanisms.
- Moved pause/badge forms into dialogs and fixed the pre-existing white-on-white Save button.

References:
- New utilities: `web/src/utils/systemState.ts`, `web/src/utils/assistantText.ts`.
- New filter components/hooks: `web/src/components/RecordToolbar.tsx`, `web/src/hooks/usePersistentFilters.ts`.
- Validation: 35 new tests, 131/131 web, `tests/test_web_api.py` 44 OK, `tests/test_ai.py` 41 OK, clean build, 14-route visual scan without technical leakage.

## Task 6: Regression cleanup and documentation

Outcome: success

Key steps:
- Fixed the old `test_execucao_nao_conhece_a_origem_totvs` failure by changing only a comment in `mes/domain/manufacturing_rules.py:32` from a specific corporate-origin reference to “sistema corporativo”; the test class then passed without behavior changes.
- Created `docs/WAVE_6_RELATORIO.md` and updated affected `AGENTS.md`, `ROADMAP.md` and API/functional docs throughout the waves.
- Work remained TEST-only; REAL was reported untouched.

Final known follow-up:
- Automatic `B1_ZMODELO` ingestion is not implemented yet.
- A definitive source for Solda delivery deadline (`prazo_entrega`) is still a future business/integration decision; this does not block current 6D UI.
- Badge sector filtering was explicitly declined; badges remain global.
- The user had explicitly accepted leaving the old Corte legacy-plan and nesting-advance behaviors unchanged.
- The user requested a concise summary rather than a long report when asking for status.
