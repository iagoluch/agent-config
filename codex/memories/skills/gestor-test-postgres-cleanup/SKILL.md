---
name: gestor-test-postgres-cleanup
description: Safely clear requested OP/task data from Gestor de Peças TESTE while preserving schema, protected records, and the real database.
argument-hint: "[scope: ops-and-tasks]"
disable-model-invocation: true
allowed-tools: [Bash]
---

# Gestor TESTE PostgreSQL cleanup

## When to use

Use only after an explicit request to clean OPs, tasks, or their derived test data in `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`. Do not use for schema changes, production cleanup, or a target whose identity cannot be verified.

## Inputs / context to gather

1. Confirm the requested data scope and the protected categories (users, configuration, AI data, reports, or others).
2. Read `app/database/config.py` and current migration/table definitions; do not print credentials.
3. Set the exact expected test database name and load `load_postgres_config(testing=True)`.

## Procedure

1. Extract only non-secret target identity from the effective test configuration, then query `current_database()` before any mutation. Require exact `GESTOR_EXPECTED_DATABASE=gestor_pecas_test` (or the user-authorized, exact test name).
2. Open the real database separately in read-only mode and record only pre-cleanup verification counts needed to prove it was not targeted.
3. Enumerate target tables and their counts. Make an explicit eligible/protected table plan from current schema/dependencies; preserve tables, migrations, indexes, constraints, users, resource/status catalogs, calendars/shifts, AI data, and reports unless explicitly in scope.
4. In one transaction, use `TRUNCATE ... RESTART IDENTITY` only on approved eligible execution/planning tables. Remove integration envelopes only when their message type is explicitly eligible; preserve `WhoIs` when cleaning `ProductionOrder` alone.
5. Before commit, verify every eligible count is zero and every protected count exactly matches its pre-count. Commit only if all checks pass.
6. Recheck the test target and read-only real target; report truncated rows separately from selective deletes.

## Efficiency plan

- Batch the test-target identity, table inventory, and protected counts before constructing the transaction.
- Stop immediately on an ambiguous DSN/name, absent test barrier, missing expected tables, or protected-count mismatch. Do not search broadly or guess table eligibility.

## Pitfalls and fixes

- Cwd looks correct but DSN points elsewhere -> abort; cwd is never proof of a safe destructive target.
- Result says only truncated count -> add selective deletes before stating a total.
- PowerShell `rg` glob returns `os error 123` -> use explicit paths or PowerShell-native file selection.

## Verification checklist

- Effective test DSN and `current_database()` match the exact expected test name.
- Real database was only read and remains unchanged.
- Eligible tables are empty; protected tables retain their original counts.
- Schema/migrations, indexes, constraints, and users were not removed.
- Report distinguishes truncation count, selective deletion count, and total.
