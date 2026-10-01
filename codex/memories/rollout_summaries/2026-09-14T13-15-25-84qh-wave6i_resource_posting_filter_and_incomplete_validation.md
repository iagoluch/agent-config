thread_id: 01a0a00e-e263-7e63-93ae-d4a579a812cd
updated_at: 2026-09-14T13:59:16+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T10-15-25-01a0a00e-e263-7e63-93ae-d4a579a812cd.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 6I validation was repeatedly interrupted and never produced a final report

Rollout context: In the TEST workspace `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, the user authorized running `PROMPT_CODEX_WAVE6I.md`, initially requiring a long observational simulation with no automatic code fixes. During execution, the user clarified that only resources with actual operator postings (“apontamento”) in the system should be shown or simulated, not every catalogued/static resource.

## Task 1: Run the Wave 6I integrated simulation

Outcome: partial

Preference signals:

- The user explicitly asked to "use apenas o que o sistema realmente aponta" and later clarified: "o que falei sobre exclusão é os recursos que nem tem apontamento no sistema" -> future runs must use canonical recorded postings as the inclusion criterion, not catalog membership, route eligibility, demand inference, API reachability, or mere existence of an OP.
- The user repeatedly insisted that the run should observe/classify rather than silently fix unrelated issues; the original prompt explicitly required no automatic code corrections and no complete test/build suites. Future agents should preserve this boundary unless the user explicitly authorizes a targeted fix.
- When the user reported that active Corte resources were absent from both Observatory and Andon, they expected active resources to appear in both views while unposted resources remain excluded -> filtering must be validated for both exclusion and inclusion cases.

Key steps:

- Read `C:\Users\iago.luchtenberg\Downloads\PROMPT_CODEX_WAVE6I.md` and followed its TEST-only execution requirements.
- Confirmed the project venv with `.venv\Scripts\python.exe -c "import psycopg; print('ok')"`; it succeeded.
- Avoided the known problematic port 8001 and used ports 8021/8022.
- First partial run: `simulation_runs\20260914_101630`; it initialized all 24 static resources, generated 162 events and 3 expected blocks, and had an empty `errors.jsonl`, but was stopped because it included resources without operational postings and had no existing CLI filter.
- A one-minute directed smoke was later reported as passing resource-selection validation and producing `selecao_postos.json`.
- The Dev Observatory filtering source was changed at `/dev-observatory/viewports`; the assistant reported 36 targeted tests passing, then 38 targeted tests passing after adding canonical Corte postings and normalizing duplicate Plasma naming.
- A later run `simulation_runs\20260914_104228` was started with the revised filtering. It showed a performance finding (`GET /operator/context` HTTP 200 in 4.076 s versus a 3 s threshold) and an API/UI divergence for one production OP, but no 5xx, timeout, or crash was reported before the run was interrupted.
- The active Corte state was eventually confirmed as Laser Ensis 3015 on plan 8478 with 28 tasks and Plasma TerraBlade 4 on plan 8818 with 8 tasks. The user reported neither appeared in Observatory or Andon; the proposed correction was to use canonical `apontamentos_corte` for Laser and Plasma.
- The final agent attempt restarted the run after reporting that Laser and Plasma appeared in both views and unposted resources were absent, but the delegated agent hit its usage limit before completion.

Failures and how to do differently:

- The initial runner opened sessions for every static resource (24 resources), including unused ones. Do not treat the runner’s static resource list as operational truth; derive the selection from canonical recorded postings before starting a long simulation.
- The first filtering interpretation was too broad: API-confirmed eligibility, queues, routes, demand, or “sem demanda” state allowed resources to appear even when they had no actual posting. The accepted rule is stricter: include only resources with a real system posting; for Corte specifically consult `apontamentos_corte`.
- The filtering fix initially hid active Laser/Plasma resources from both Observatory and Andon. Any filtering change needs a two-sided acceptance test: named unposted examples from the screenshot must have zero occurrences, while actively posted Laser/Plasma resources must appear in both endpoints.
- The Wave 6I simulation never completed after the final restart because the delegated agent hit its usage limit. There is no verified final `report.md`, no final event/OP/error summary, and no validated status for all five requested coverage areas.
- The rollout drifted from the original “observe only/no code changes” instruction after the user explicitly selected the first option to adjust execution/configuration, then targeted view/filter changes were applied. Future agents should clearly separate authorized presentation/filter fixes from forbidden simulation-result fixes and document every changed file before resuming a long run.

Reusable knowledge:

- Correct environment command: `.venv\Scripts\python.exe` (system Python lacks `psycopg`).
- Avoid port 8001 on this machine; use `--api-port 8021 --observatory-port 8022` or another free pair.
- The user’s accepted operational truth is the system’s actual posting records. For ordinary operator resources use canonical operational postings/sessions; for Corte use `apontamentos_corte`.
- The Dev Observatory viewport source was identified as `/dev-observatory/viewports`; the relevant filtering behavior is presentation-level and must not delete database records, OPs, or history.
- Named acceptance examples from the screenshots included unused inventory-like cards such as AC VX, ACOPLA, ALMOX, BICOS, BRAÇO, and CAB; these should remain absent when they have no posting.
- Active examples that must remain visible when posted: Laser Ensis 3015 and Plasma TerraBlade 4. Duplicate Plasma representations were reported and normalized through a canonical map.
- The only concrete performance finding reported was `GET /operator/context` returning HTTP 200 in 4.076 seconds, above the 3-second threshold; it was classified as an observational performance finding, not a timeout or functional failure.

References:

- Prompt: `C:\Users\iago.luchtenberg\Downloads\PROMPT_CODEX_WAVE6I.md`
- Initial partial run: `simulation_runs\20260914_101630` (162 events, 3 expected blocks, empty `errors.jsonl`, no `report.md`).
- Later active run: `simulation_runs\20260914_104228`.
- Venv check: `.venv\Scripts\python.exe -c "import psycopg; print('ok')"`
- Simulation shape specified by the prompt: `.venv\Scripts\python.exe scripts\run_simulacao_industrial.py --duration 60m --factory-duration 8h --seed 20260912 --api-port 8021 --observatory-port 8022`
- User wording: "use apenas o que o sistema realmente aponta"; "o que falei sobre exclusão é os recursos que nem tem apontamento no sistema".

## Task 2: Apply strict resource visibility filtering

Outcome: partial

Preference signals:

- The user said resources with no operator posting should be excluded, not merely hidden based on inferred demand or catalog state -> future filtering should be keyed to recorded postings and should preserve active posted resources.
- The user specifically checked whether Corte/Laser/Plasma were running and objected when they were absent from both screens -> always verify active-resource visibility in both Observatory and Andon after changing filters.

Key steps:

- Initial Andon behavior was traced to automatic “sem demanda” states and inventory-wide rendering, which caused unused cards to be shown.
- A presentation-level filter was applied to `/dev-observatory/viewports`, without deleting operational database records.
- Smoke checks reportedly showed no screenshot-listed unused resources, and later checks reported active Plasma visible in both views; duplicate Plasma naming was normalized.
- The final stricter implementation was reported to use canonical postings/sessions plus `apontamentos_corte` for Laser and Plasma.

Failures and how to do differently:

- Do not claim the filter is complete based only on a smoke or targeted tests; the final Wave run did not complete and the actual repository diff was not included in the rollout evidence.
- Do not remove active resources merely because they lack a generic posting table entry if they have a valid Corte posting in `apontamentos_corte`.
- Validate both contracts independently: Observatory and Andon must agree for every active posted resource and must both exclude every unposted resource.

Reusable knowledge:

- The desired behavior is a projection/view filter, not destructive deletion: preserve database records, OPs, and history; remove only resources without canonical postings from the operational views.
- Canonicalization is necessary because the same Plasma station appeared under different names and produced duplicate Andon entries.

References:

- Presentation source named in the rollout: `/dev-observatory/viewports`.
- Active resources cited: `Laser Ensis 3015`, plan `8478`, 28 tasks; `Plasma TerraBlade 4`, plan `8818`, 8 tasks.
- Reported targeted validation counts: 36 tests after the initial viewport filter; 38 after canonical Corte posting support and Plasma normalization.
