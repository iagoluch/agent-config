thread_id: 01a0ceec-b220-7e61-91a7-7aa03615e0c7
updated_at: 2026-09-23T18:04:24+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\23\rollout-2026-09-23T12-40-13-01a0ceec-b220-7e61-91a7-7aa03615e0c7.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes
git_branch: master

# Auditoria técnica do Gestor de Peças avançou, mas não foi concluída

Rollout context: O objetivo era validar e corrigir 21 achados de auditoria no repositório `Gestor de Peças - Area de Testes`, sem tocar no banco REAL, usando TESTE e sem criar tags `v*`.

## Task 1: Localizar relatório e validar escopo

Outcome: partial

Preference signals:
- O usuário interrompeu a delegação dizendo: "esses agentes vão acabar com o meu uso" -> em tarefas futuras, evitar subagentes salvo pedido explícito e trabalhar sozinho quando possível.
- O usuário pediu para finalizar apenas se estivesse "seguro" para deixar o Claude continuar e fornecer "um contexto de TUDO" -> preservar WIP, fazer handoff detalhado e não declarar auditoria concluída sem evidência completa.

Key steps:
- O objetivo anexado foi lido integralmente.
- O relatório F1–F21 não estava no anexo nem no repositório; foi localizado em sessão/artefato do Claude e reconstruído como `auditoria_completa_23_09_2026.md`.
- A árvore inicialmente estava em `cb87579`; alterações posteriores foram feitas em commits separados.

Failures and how to do differently:
- A primeira tentativa tratou a ausência do relatório como bloqueio; a busca em sessões Claude e artefatos locais encontrou evidência adicional.
- Não presumir que `docs/AUDITORIA_SEGURANCA_2026-09-14.md` seja o relatório F1–F21; é uma auditoria diferente.

Reusable knowledge:
- O projeto exige leitura inicial de `AGENTS.md`, `ROADMAP.md`, `docs/STATUS_ATUAL.md` e estado Git.
- Regras industriais e contratos TOTVS devem ser confirmados por documentação/histórico, nunca inferidos de payloads ambíguos.

References:
- CWD: `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`
- Commits relevantes: `8f0aa6c` (SOAP/Dev Observatory fail-closed), `76c2cac` (backup TESTE), `b3b0fb8` (identidade imutável).

## Task 2: Segurança fail-closed — SOAP TOTVS e Dev Observatory

Outcome: success

Key steps:
- SOAP inbound passou a exigir `GESTOR_TOTVS_SOAP_ALLOWED_SOURCE_CIDRS`, validando o peer TCP observado; `Host` e `X-Forwarded-For` não são usados para autenticação.
- Allowlist ausente mantém a aplicação ativa, mas retorna `503` para WSDL e POST antes de ler o corpo.
- Dev Observatory passou a recusar credenciais com privilégios efetivos de escrita/DDL, além de `default_transaction_read_only=on` e prova de escrita recusada pelo PostgreSQL.
- Validação: `tests.test_totvs_integration` (39 testes) e `tests.test_dev_observatory` (20 testes); conjunto combinado de 59 testes passou.
- Instância temporária em `:8002` confirmou `health=200` e WSDL SOAP `503` sem allowlist.

Failures and how to do differently:
- O processo existente em `:8001` estava executando código anterior e continuou retornando WSDL `200`; reinício automático foi bloqueado pela política local. Validar/reiniciar explicitamente antes de usar o serviço.

Reusable knowledge:
- Falta configurar o IP/CIDR real do servidor Protheus; não preencher com valor inventado.
- Falta criar role PostgreSQL dedicada somente leitura para habilitar Dev Observatory REAL.

References:
- `.env.example`: `GESTOR_TOTVS_SOAP_ALLOWED_SOURCE_CIDRS`
- `backend/integrations/totvs_soap.py`
- `backend/api/config.py`
- `backend/observability/readonly_db.py`
- Commit: `8f0aa6c`

## Task 3: Backup verificável do banco TESTE

Outcome: partial

Key steps:
- Criado `scripts/backup_banco_teste.py`, com confirmação literal de `gestor_pecas_test`, dump PostgreSQL custom, manifesto SHA-256 e validação `pg_restore --list`.
- Criado `docs/BACKUP_TESTE.md` e testes `tests/test_backup_banco_teste.py`.
- Backup real TESTE criado em `backups/test/`, 5.093.524 bytes, SHA-256 `d75e3c3eb53f1f0ed29e36e5523529764f0f3a547856c21e90369d842c3ca08d`.
- Validação: 10 testes de backup/reset passaram.

Failures and how to do differently:
- Ainda não houve restauração em banco descartável, agendamento, retenção ou cópia externa; F21 permanece parcialmente resolvido.

References:
- Commit: `76c2cac`
- `scripts/backup_banco_teste.py`
- `docs/BACKUP_TESTE.md`
- `backups/test/` é ignorado pelo Git.

## Task 4: Handoff e estado final

Outcome: partial

Preference signals:
- O usuário pediu para não interferir no trabalho do Claude e preservar seu WIP -> não incluir no commit nem sobrescrever: `docs/STATUS_ATUAL.md`, `web/src/layouts/OperatorShell.tsx`, `web/src/styles/global.css`, `web/src/test/operator.test.tsx`, `web/src/test/quality.test.tsx`.

Key steps:
- Objetivo foi pausado explicitamente via `update_goal(status="paused")`.
- Foi entregue handoff indicando que F18 continua sem contrato TOTVS suficiente e que há gates externos restantes.

Failures and how to do differently:
- A auditoria completa não foi concluída; não declarar sistema pronto para produção/merge sem fechar CIDR SOAP, role DevObs, contrato F18 e política de restore/DR.

Reusable knowledge:
- F18 não deve desativar OPs com base apenas em `StatusOrderType` ou ausência de snapshot; falta contrato oficial de cancelamento/delete/estado terminal.
- O worktree final contém WIP Web não relacionado; qualquer continuação deve preservá-lo e revisar `git status` antes de editar.

References:
- Pendências registradas em `docs/STATUS_ATUAL.md`.
- Processo atual em `:8001` precisa ser reiniciado para refletir `8f0aa6c`/`76c2cac`.
