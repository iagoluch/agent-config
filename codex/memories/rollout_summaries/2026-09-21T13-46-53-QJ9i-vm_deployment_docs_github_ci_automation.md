thread_id: 01a0c438-36cf-7653-bc98-2ec79e66b384
updated_at: 2026-09-18T20:07:30+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\21\rollout-2026-09-21T10-46-53-01a0c438-36cf-7653-bc98-2ec79e66b384.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# VM deployment documentation and GitHub automation were established

Rollout context: Windows workspace `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, repository `iagoluch/gestor-de-pecas`, branch `master`.

## Task 1: Validate VM infrastructure requirements

Outcome: success

Key steps:
- Compared the proposed infrastructure document against `requirements.txt`, `compose.yaml`, `README.md`, `docs/WEB_DEPLOYMENT.md`, and scheduler/outbox code.
- Confirmed PostgreSQL 17, FastAPI/Uvicorn, ODBC integration, static React build served by FastAPI, and one Uvicorn process are aligned with the current system.
- No repository changes were needed for the technical approval.

Reusable knowledge:
- Production recommendation remains 8 vCPU, 16 GB RAM, 200 GB SSD/NVMe, Ubuntu Server 26.04 LTS, PostgreSQL 17, Nginx, Python 3.14, and one Uvicorn process.
- Node.js is needed for building the frontend, not for runtime production execution.
- Internal tasks/outbox behavior makes multiple Uvicorn workers unsafe without further coordination.

## Task 2: Automate GitHub synchronization and CI

Outcome: success

Key steps:
- Configured `origin` to `https://github.com/iagoluch/gestor-de-pecas.git`.
- Added a `post-commit` hook that automatically pushes commits.
- Added `.github/workflows/ci.yml` for backend tests and frontend build/tests.
- Resolved CI issues involving the required `test` database name, runner timezone, quality-test timing, and tests depending on shared real data.
- Final CI result was confirmed green: 1027 backend tests, `OK` with skips.

Failures and fixes:
- `TEST_DATABASE_URL` must contain `test` in the database name.
- GitHub runners use UTC; set `TZ=America/Sao_Paulo` in the CI job to match the application/PostgreSQL session timezone.
- Tests with enabled TOTVS outbox require a controllable/injected clock for the 60-second minimum duration.
- Tests auditing shared TOTVS/SigmaNEST data must skip when the disposable CI database has no such data.

## Task 3: Clean GitHub repository contents

Outcome: success

Key steps:
- Changed the GitHub default branch from `main` to `master` and deleted the obsolete `main` branch.
- Removed Protheus source files, integration reference data, reports, local datasets, and simulation configuration from current tracking.
- Corrected `.gitignore`, including the `outputs/` directory and local tool caches.
- A historical credential exposure was identified, but the user explicitly chose not to rewrite history or rotate it because it was a disposable homologation environment.

## Task 4: Prepare VM deployment automation

Outcome: success

Key steps:
- Added `.github/workflows/deploy.yml`.
- Deployment is intentionally triggered only by release tags (`v*`), not every push.
- The workflow is designed for a self-hosted runner installed inside the VM, avoiding inbound SSH exposure from GitHub.
- The VM does not yet exist; the workflow is prepared and waits for provisioning and runner registration.

## Task 5: Create VM deployment documentation

Outcome: success

Key steps:
- Added `docs/REQUISITOS_INFRAESTRUTURA_VM.md` with the approved infrastructure requirements and deployment preparation information.
- Created a user-requested DOCX, `Gestor_de_Pecas_Guia_Implantacao_VM.docx`, explaining the deployment in simpler prose rather than as a literal checklist and excluding credentials or leaked-secret details.
- Final documentation cleanup removed references to rotating an exposed TOTVS password.
- The final documentation commit was `0709c14`, automatically pushed to GitHub.

References:
- `docs/WEB_DEPLOYMENT.md`
- `docs/REQUISITOS_INFRAESTRUTURA_VM.md`
- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`
- `scripts/package_web_release.py`
- Final commit: `0709c14 docs: remove referência à senha exposta do requisitos de infraestrutura`
