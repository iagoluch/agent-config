thread_id: 01a0d8ca-708f-7902-8f00-20545c9b8fd3
updated_at: 2026-09-25T13:17:24+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\25\rollout-2026-09-25T10-39-00-01a0d8ca-708f-7902-8f00-20545c9b8fd3.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Corrigiu recursos presos fora de turno e restringiu a Consulta Operacional aos postos apontáveis

Rollout context: Projeto Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, usando o banco TEST `gestor_pecas_test` e servidor local na porta 8001.

## Task 1: Corrigir recursos reais presos em Fora Turno

Outcome: success

Key steps:
- Identificou que 75 recursos estavam vinculados ao calendário residual `ETAPA4B_TESTE_20260831`, que só tinha turnos na segunda e terça.
- O commit `c99f31b` excluía recursos com calendário próprio do retorno global das 08:00; por isso recursos reais como LASER1 e PLASMA ficaram em `fora_turno` na sexta-feira.
- Desvinculou os 75 recursos no TEST, salvando backup dos vínculos.
- Verificou que o ciclo seguinte fechou `fora_turno` em 25/09 08:00 e abriu `fila / retorno_turno_sem_demanda`; nenhum recurso permaneceu em Fora Turno.
- REAL não tinha vínculos de calendário e não foi afetado.

Reusable knowledge:
- O servidor 8001 usa `TEST_DATABASE_URL`, não `DATABASE_URL`; confirmar o banco efetivo antes de diagnosticar dados.
- Recursos com calendário próprio seguem exclusivamente esse calendário; não aplicar fallback global sem validar, pois isso quebraria calendários legítimos.

## Task 2: Mostrar somente recursos apontáveis na Consulta Operacional

Outcome: success

Preference signals:
- O usuário pediu: “se suma com esses recursos não utilizados e foque na regra que eu ja passei sobre quais recursos são usados.” Isso confirma que o critério deve ser postos apontáveis definidos em `OPERATOR_SECTORS`, e não histórico incidental de uso ou todo o catálogo sincronizado.

Key steps:
- Substituiu o filtro baseado em `listar_recursos_com_uso()` pela regra central `is_apontavel_resource`, derivada dos postos de `OPERATOR_SECTORS` e códigos de estação.
- Manteve uma proteção: recurso produzindo agora, com OP ativa ou com conta de operador ativa não desaparece.
- Removido o método obsoleto `Database.listar_recursos_com_uso`.
- Ligou o filtro nos endpoints `/operations/overview`, `/operations/resources` e `/operations/stream`.
- No TEST, a consulta caiu de 386/388 recursos para 34 postos apontáveis; recursos “Não disponível”, catálogo nunca usado e os 41 códigos legados de Solda Aço desapareceram.
- Corrigiu a identidade duplicada de Pintura: “Secagem” da conta é o mesmo posto que `ESTUFA`, usando `station_resource_code`/`_post_identities`.
- ROBO P e ROBO S foram consolidados em um único card “Robô 1”, preservando as OPs e escolhendo o estado mais relevante.
- Foram aprovados 194 testes relacionados; a API do servidor reiniciado respondeu 200 para `/api/v1/operations/resources`.

Failures and how to do differently:
- O processo antigo da porta 8001 não tinha `--reload`, então a tela continuava mostrando 388 apesar do código novo. Reiniciar o servidor ou usar a configuração `gestor-dev-observatory-8001` com reload é necessário após mudanças.
- Não foi feita confirmação visual autenticada porque a tela exigia login; a validação foi feita diretamente no TEST e pelos logs/API.

References:
- `app/core/operator_sectors.py`: `OPERATOR_SECTORS`, `WELDING_FAMILY_SECTORS`, `is_apontavel_resource`.
- `mes/services/frontend_facade.py`: parâmetro `somente_recursos_em_uso`, `_merge_shared_post_cards`, `_post_identities`.
- `backend/api/routers/operations.py`: filtro habilitado nos três endpoints.
- `app/core/resource_mapping.py`: `shared_post_name`, `station_resource_code`, nomes operacionais.
- Testes: `python -m pytest tests/test_andon_redesign.py tests/test_web_api.py tests/test_stage4b_factory_shift.py tests/test_execution_to_management_consistency.py tests/test_dev_observatory.py tests/test_stage4c_resource_registry.py tests/test_resource_state_no_demand_and_break.py -q -p no:cacheprovider` → `194 passed`.


