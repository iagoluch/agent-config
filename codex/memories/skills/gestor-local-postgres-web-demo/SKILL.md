---
name: gestor-local-postgres-web-demo
description: Recover Gestor de Peças local Docker PostgreSQL or safely build/start/restart/verify the current TESTE Web on 15432/8001; use when TEST_DATABASE_URL, local server scripts, or a requested Cloudflare Quick Tunnel is involved.
argument-hint: "[recover-postgres|start-test-web|verify|quick-tunnel]"
disable-model-invocation: true
allowed-tools: [Bash]
---

# Gestor local PostgreSQL and Web demo

## When to use

Use for the active Gestor de Peças checkout when local PostgreSQL is unreachable, Docker reports a bind/port problem, the Web must start against the official test database, or a temporary Cloudflare URL is requested. Do not use it to reset/truncate data, expose a password, or target operational `gestor_pecas` with the Web API.

## Inputs / context

1. Confirm the effective checkout is `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes` and the requested mode. The old profile path is historical evidence only.
2. Read `.env` and `compose.yaml` without printing password values. Extract only host, port, database, and user from DSNs.
3. Treat port reservations, container state, and exact DB counts as machine/time-specific; inspect them before modifying anything.

## Procedure

1. Inspect Docker and mapping: `docker info`, `docker compose ps -a`, and `netsh interface ipv4 show excludedportrange protocol=tcp`.
2. Compare the external Compose port with `.env`. The most recently validated mapping was `127.0.0.1:15432:5432`; `54321` fell in a Windows excluded range. Do not assume a previously working port remains free after reboot.
3. If Docker Desktop itself fails after a Windows-profile migration, inspect `AppData\Local\Docker\run` and `AppData\Local\docker-secrets-engine` for migrated stale Unix sockets. Move only those ephemeral folders reversibly to a recovery set, then retry Docker; never factory-reset Docker or touch its VHD/volume.
4. For recovery, recreate only PostgreSQL: `docker compose up -d --force-recreate postgres`. Preserve `gestor_postgres_data`; do not delete volumes or change database/user credentials.
5. Verify TCP with `Test-NetConnection -ComputerName 127.0.0.1 -Port 15432`, then validate with the project configuration loader plus psycopg and a read-only `SELECT 1`.
6. Before starting or changing a Web instance, inspect the listener/process and effective DSN. The current validated target is `gestor_pecas_test` at `127.0.0.1:15432`; `gestor_pecas` is real and must remain separate. Never recreate the deleted former demo DB `gestor_pecas_test_simulacao_residencia_20260824` from stale notes.
7. For current direct test startup, set `GESTOR_EXPECTED_DATABASE=gestor_pecas_test`, retain `TEST_DATABASE_URL`, set `GESTOR_SIMULATION_MODE=0`, and start `C:\Python314\python.exe -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8001`. Use `GESTOR_WEB_SERVE_STATIC=1`, allowed hosts, and secure cookie/public-host settings only as needed by the requested Web exposure. Do not use `tests\simulacao_historica_3_meses\run_web_simulacao.py`: it requires `SIMULACAO_DATABASE_NAME` for a separate simulation database.
8. If 8001 is occupied or looks stale, inspect `Get-NetTCPConnection -LocalPort 8001 -State Listen`, identify the exact owning PID/process, and stop only that process when the user authorized recovery. Confirm the listener is gone before continuing; do not kill processes indiscriminately.
9. Prefer the current local lifecycle scripts: `tools/iniciar_servidor.py`, `tools/reiniciar_servidor.py`, and `tools/parar_servidor.py`. They start PostgreSQL Compose and uvicorn at `127.0.0.1:8001` without Cloudflare or `.env` mutation. For both frontend and backend changes, run `python reiniciar_build.py` from checkout root: it runs `tsc -b` and Vite build first, then invokes the official restart; a failed build must stop before restart. Uvicorn has no `--reload`, so Python changes require restart. Use the legacy Cloudflare launcher only when a temporary public tunnel is explicitly requested.
10. Verify `http://127.0.0.1:8001/`, then `/api/v1/system/health` and `/api/v1/system/capabilities`. Do not use `/api/v1/health` as proof because the SPA may return HTML there. Confirm `status=ok`, database available, a schema compatible with the checkout, and `active_data_source=postgresql_test_only`.
9. For an authorized temporary public tunnel, run `cloudflared tunnel --url http://127.0.0.1:8001 --no-autoupdate` and validate the same root, health, and capabilities endpoints through the generated hostname. Treat every `trycloudflare.com` hostname as temporary; do not stop an existing 8000/8001 process or tunnel unless requested.

## Efficiency plan

- Run the Docker state, port reservation, and Compose inspection once as the first batch.
- Parse DSNs programmatically but log only host/port/database/user.
- Stop at the first failed layer: Docker engine → published TCP → effective DSN → Web health → capabilities. Do not troubleshoot Wi-Fi if the DSN is loopback; do not infer the live DB from `.env` when a process override is possible.

## Pitfalls and fixes

- Timeout or Docker bind error with no owning process -> check `excludedportrange`; select/recreate on a non-excluded published port and update only the port in the DSN.
- `/` is HTTP 200 but health is 503 -> the SPA is being served while `TEST_DATABASE_URL` is stale; verify the effective DSN and restart against the test-named DB.
- Database name includes literal `$1` after a substitution -> parse it and repair the DSN before launch.
- Port 8000 cannot stop and returns 503 -> an old process may reference a deleted DB; stop it using its owning service or an elevated PowerShell. Do not retry the same non-elevated session.
- API rejects the database -> the name must include `test`; never substitute operational `gestor_pecas`.
- `Start-Process` refuses simultaneous stdout/stderr redirection -> start the official supervisor directly, then validate root and `/api/v1/system/health` externally.
- `Barreira de segurança: o alvo não é exclusivo da homologação.` -> retain the guard and correct `TEST_DATABASE_URL`; it is not a condition to bypass.
- Docker Desktop fails immediately after profile migration -> stale migrated sockets are likely; move only `Docker\run` and `docker-secrets-engine` reversibly, then recheck Docker before Compose.

## Verification checklist

- Docker engine is available and `postgres` is healthy.
- Actual TCP port is listening and psycopg/read-only connection succeeds.
- No credentials were printed or stored.
- The current official DB is explicitly `gestor_pecas_test`, confirmed from the listener/effective DSN, and operational `gestor_pecas` was not targeted.
- `/` is HTTP 200, `/api/v1/system/health` reports database available and a schema compatible with the checkout, and capabilities report `postgresql_test_only` on port 8001.
- After frontend/backend changes, the build passed before restart and health confirms the restarted TESTE instance, not a stale listener.
- When a public URL was requested, its root, health, and capabilities endpoints also succeeded; its temporary hostname was reported as ephemeral.
