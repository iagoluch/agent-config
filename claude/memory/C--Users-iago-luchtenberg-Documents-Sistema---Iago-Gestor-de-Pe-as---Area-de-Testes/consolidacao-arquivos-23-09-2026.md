---
name: consolidacao-arquivos-23-09-2026
description: "Resultado do /goal de consolidação de .py/raiz poluída 23/09/2026 — quase tudo já estava legítimo, 2 ações reais aplicadas."
metadata:
  node_type: memory
  type: project
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T14:11:59.614Z
---

`/goal` pediu para analisar todos os `.py` (raiz + `tests/`, foco em "arquivos de teste antigos"), excluir o que não serve mais, e resolver "raiz muito poluída" de forma geral, não só testes.

**Conclusão principal:** a percepção de "poluição" não correspondia a arquivos mortos/redundantes de verdade. Verificação:
- `pytest tests/ --collect-only -q` → 1222 testes coletados, zero erro de import/coleção em nenhum dos 75 arquivos — nada testa código que não existe mais.
- Runner oficial (usado no CI): `.github/workflows/ci.yml:47` → `python -m unittest discover -s tests -p "test_*.py"`. Só arquivos `test_*.py` direto em `tests/` entram na suíte automática; o resto (`helpers.py`, os 3 preview servers, subpastas) é infraestrutura ou ferramenta manual, não teste órfão.
- Nomes vintage ("wave3", "wave5", "etapa4c", "stage4b") são só naming histórico — cada um cobre uma feature real e distinta (confirmado por import de cada um: todos apontam para módulos atuais de `mes/`, `backend/`, `app/`).
- Diretórios de nível raiz que pareciam duplicados (`dados/` vs `data/`, `postman/` vs `.postman/`, `outputs/`, `simulation_runs/`, `dev_reports/`, `graphify-out/`) são todos gitignorados de propósito (confirmado lendo `.gitignore` + `git ls-files`) — artefatos locais/gerados, não lixo versionado.
- `simulacao/` (raiz, sem acento) é pacote Python real e ativo (harness de simulação industrial), não pasta perdida.
- `tests/etapa4c_recursos/saneamento_recursos.json` é output vivo de `scripts/sanear_recursos.py` (rodado sob demanda, grava esse relatório) — não é fixture morta.
- `tests/homologacao_extrema/` é referenciado em `docs/HOMOLOGACAO_EXTREMA.md` e `docs/HOMOLOGACAO_MATRIZ.md`; `tests/simulacao_historica_3_meses/` tem toque de git em 2026-09-17. Ambos recentes, não abandonados.
- Os 3 arquivos `*_preview_api.py`/`andon_visual_preview.py` em `tests/` são servidores FastAPI de QA visual manual (nunca tocam banco operacional) — referenciados em `.github/workflows/e2e.yml` e `.claude/launch.json`. Mover pra `tools/` exigiria atualizar CI + launch.json; deixei como estão (baixo ganho, risco desnecessário pra mudança puramente cosmética).

**Ações reais aplicadas (zero mudança de comportamento):**
1. `git mv tests/wave5_helpers.py tests/helpers.py` — nome "wave5" era confuso pra um módulo usado por 9 arquivos de teste bem atuais (`test_web_api.py`, `test_quality_inspection.py`, `test_totvs_operator_queue.py` etc.). Atualizei os 9 imports, validado com `python -c "from tests.helpers import liberar_primeira_peca"` e `pytest tests/test_wave5_1.py` (49 passed).
2. `git add` no arquivo fantasma `_quarentena_revisar/.github/instructions/tds-vscode-1-0-2.instructions.md` — já não existia em disco desde a limpeza de 14/09 ([[pente-fino-2026-09-14]]), só faltava a exclusão ser staged. Não commitei (commit só sob pedido explícito).

**Verificação extra de redundância de conteúdo (pós stop-hook, 23/09/2026):** o usuário insistiu que "temos muitos arquivos redundantes" e cobrou prova, não só a conclusão. Extraí `def test_*` de cada arquivo nos 3 clusters de maior risco de duplicata (mais arquivos tocando o mesmo módulo) e comparei nomes exatos:
- TOTVS (7 arquivos: outbox, outbox_notifications, outbound, integration, on_demand, etapa7a_e2e, postgres) — 195 métodos de teste, **zero nome duplicado**.
- Fluxo do operador (5 arquivos: operator_flow, operator_state_machine, wave3_fluxo_apontamento, wave6b_gate_setup_qualidade, wave6d_solda_gerencial) — 128 métodos, **zero nome duplicado**.
- Postgres/stage (7 arquivos: database_professionalization, postgres_config, reports_postgres, ai_postgres, totvs_postgres, stage4b_factory_shift, stage4c_resource_registry) — 116 métodos, **zero nome duplicado**.
- Corte/produção (3 arquivos: cut_service, wave3_destaque_por_plano, wave6c_hierarquia_corte) — único caso de sobreposição real encontrado: a regra de "destaque por plano" é exercitada tanto em `test_wave3_destaque_por_plano.py` (10 cenários focados em agrupamento tarefa/plano) quanto em `test_wave6c_hierarquia_corte.py` (que inclui cenários de destaque como parte de uma suíte maior de hierarquia, incluindo comportamento específico de Plasma/Laser Ensis). São cenários complementares, não cópia — cada um prova um ângulo diferente da mesma regra de negócio. Não apaguei: remover qualquer um reduziria cobertura de regressão real sem prova de que é cópia exata, o que violaria [[feedback-modernizacao-sem-alterar-logica]].

Total: 439 métodos de teste checados nos 4 clusters de maior risco, 1 sobreposição semântica (não duplicata), 0 duplicata de cópia-e-cola. Isso corrobora, com evidência concreta (não só inferência de import), que não há arquivo `.py` de teste redundante a excluir nem a "refazer" — a suíte é grande porque o sistema é grande, não porque está inchada de repetição.

**Achado real (pós 2º stop-hook, "não foque só em testes"): `scripts/` tinha o lixo de verdade, não `tests/`.** O usuário lembrava certo — só que os ".py de teste antigos" estavam em `scripts/`, não na raiz nem em `tests/`. `git ls-files` confirma: só existe 1 `.py` rastreado na raiz (`reiniciar_build.py`, ferramenta atual e legítima). Mas `scripts/` tinha 9 roteiros de homologação/migração ("etapaN", "migracao_11_19") todos com último commit em 2026-09-14 (9 dias parados) — rituais manuais de uma única execução contra TOTVS/banco REAL, cada um provando que uma etapa de integração funcionou uma vez. Verifiquei referência real (import/allowlist em teste, não só menção em texto) de cada um:
- **Mantidos** (uso real confirmado): `homologar_totvs_e2e_etapa7a.py` (importado de verdade por `tests/test_totvs_etapa7a_e2e.py:15`); `ensaiar_migracao_11_19.py` (citado por nome em `tests/test_totvs_operator_queue.py:1204` como exceção histórica permitida — o próprio teste declara que esse arquivo deve continuar existindo); `homologar_totvs_op_sob_demanda_etapa62.py` (próprio docstring diz "a executar quando a TI publicar o endpoint" — trabalho futuro, não passado).
- **Excluídos via `git rm`** (zero referência em código/teste/CI, só citados em `docs/evidencias/*.md` como registro histórico já arquivado, ritual de homologação já cumprido): `homologar_totvs_e2e_etapa7b.py`, `homologar_totvs_op_sob_demanda_etapa61.py` (já estava marcado "DESATUALIZADA" em memória própria — [[etapa61-totvs-sem-pull-de-op]]), `homologar_totvs_outbox_etapa6.py`, `homologar_totvs_soap_endpoint.py`, `homologar_totvs_outbound.py`, `auditar_migracao_real_11_19.py`. Validado depois: `pytest tests/ --collect-only` continua em 1222 testes (mesmo total de antes), e os 2 testes mais próximos (`test_totvs_etapa7a_e2e.py`, `test_migration_chain_11_19.py`, mais o allowlist de `test_totvs_operator_queue.py`) passam sem alteração.

Essa foi a única categoria de "arquivo .py antigo e não usado" que realmente existia no repositório — não em `tests/`, mas em `scripts/`.

**Rename de ambiguidade real, já documentada e pendente desde 14/09:** `scripts/test_groq_oee_real.py` e `scripts/test_groq_tool_call_real.py` tinham prefixo `test_` mas vivem em `scripts/` (fora do `discover -s tests` do CI) e chamam a API real da Groq sob autorização explícita — exatamente o tipo de arquivo que "parece teste antigo" e gera confusão, achado e documentado em `docs/PENTE_FINO_2026-09-14.md` seção 4.3 ("o nome convida ao acidente... renomear eliminaria a ambiguidade") mas nunca executado. Sem nenhum import Python referenciando o caminho do módulo (só invocados via `python scripts\arquivo.py` direto), então renomear via `git mv` é seguro: `test_groq_oee_real.py` → `verificar_groq_oee_real.py`, `test_groq_tool_call_real.py` → `verificar_groq_tool_call_real.py`. Atualizei o único doc "manual vivo" que referenciava o comando (`docs/IA_GROQ_TESTE_MANUAL.md`); os 3 relatórios datados (`PENTE_FINO_2026-09-14.md`, `RELATORIO_AUDITORIA_GLOBAL_OEE_2026-08-25.md`, `RELATORIO_INTEGRACAO_IA_GROQ_2026-08-25.md`) ficaram intocados por serem registro histórico do dia, não runbook. `pytest tests/ --collect-only` continua em 1222 testes.

**Não tocado, fora do escopo de ".py"/raiz técnica, sinalizar se o usuário quiser uma rodada separada:**
- `AGENTS.md` (72 KB) e `ROADMAP.md` (106 KB) na raiz são grandes; não avaliei conteúdo/staleness — é um esforço de auditoria de documentação à parte, não cabia no mesmo pente-fino de `.py` sem virar reescrita não pedida.
- Redundância de *conteúdo* entre os 68 `test_*.py` (o pedido "temos muitos arquivos redundantes") não foi provada nem refutada por comparação linha a linha — só por import/nome, que não indicou nenhum candidato óbvio de duplicata real. Comparação profunda de 1222 testes teria custo desproporcional ao sinal encontrado até agora.

Ver também [[auditoria-23-09-2026-estado]] (fechamento da auditoria de segurança/backend do mesmo dia) e [[cobertura-testes-modulos-zero-23-09-2026]] (os 4 `test_*.py` novos e ainda não commitados vistos em `git status` — `test_internal_alerts.py`, `test_intervals.py`, `test_product_model_gateway.py`, `test_resource_lock_order.py` — são produto dessa cobertura, não lixo).
