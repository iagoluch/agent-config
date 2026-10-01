thread_id: 01a09ff5-200d-7822-aa4b-afdfb24dcb73
updated_at: 2026-09-08T22:53:06+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\14\rollout-2026-09-14T09-47-17-01a09ff5-200d-7822-aa4b-afdfb24dcb73.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Wave 4 foi fechada no ambiente TESTE, sem promoção do REAL

Rollout context: O usuário pediu para continuar exatamente do estado da Wave 4, corrigir contratos Web antigos, aplicar/validar a migration 25 apenas em `gestor_pecas_test`, executar todas as validações e não tocar no REAL nem inventar dados SigmaNEST. Durante o rollout, o usuário posteriormente decidiu que `boas + refugo` não pode exceder o planejado e autorizou escalar para `extreme`, mas também pediu para parar e salvar o estado. Após a retomada, o agente concluiu os bloqueios técnicos; nenhuma promoção, backup ou preflight do REAL foi executado.

## Task 1: Fechamento técnico da Wave 4

Outcome: success

Preference signals:

- O usuário instruiu: "Continue a Wave 4 exatamente do estado atual", "NÃO altere novas regras funcionais" e "NÃO inicie promoção do banco REAL" -> em tarefas de fechamento, preservar o escopo existente, não introduzir regras novas e manter o ambiente produtivo intocado até as validações combinadas.
- Quando perguntado sobre o limite, o usuário escolheu: "Não, teto é o planejado" -> tratar `boas + refugo <= quantidade planejada` como regra confirmada; não relaxar a CHECK nem transformar o `ValueError` em mero aviso.
- O usuário escolheu escalar para `extreme, sem promoção` -> resolver bloqueios de causa raiz e manter a promoção do REAL separada, condicionada a testes verdes, backup/restauração e OK final.
- O usuário pediu: "pare e salve aonde parou, preciso sair" -> agentes devem suportar parada segura e deixar um estado persistido e retomável, sem presumir que o trabalho em background terminou.
- O rollout reforçou: "não inventar datas SigmaNEST" e não iniciar cenário de fábrica -> dados não comprovados devem continuar explicitamente bloqueados, não preenchidos por inferência.

Key steps:

- Os testes Web antigos foram alinhados ao comportamento Wave 4 sem alterar produção Web indevidamente; resultado final: `npm test` com **80/80**, 7 arquivos.
- A migration 25 foi aplicada somente em `gestor_pecas_test`, levando o schema de 24 para 25.
- Foi validada a coluna `apontamentos_operacionais.etapa_anterior_pendente_confirmada BOOLEAN NOT NULL DEFAULT false`, o índice parcial `idx_apontamentos_override_roteiro` e a CHECK `quantidade_boa + quantidade_refugo <= quantidade`, mantida `NOT VALID` por projeto.
- O bug do Andon foi corrigido na causa raiz: `listar_cortes_ativos_andon` deixou de buscar `sigmanest_repeat_id` em `apontamentos_corte` e passou a fazer `LEFT JOIN catalogo_sigmanest_planos_corte`, expondo o campo neutro `repeticao`.
- A camada `mes/services/andon.py` passou a consumir `repeticao`; o guard arquitetural sobre vocabulário corporativo voltou a passar. O frontend não precisou ser modificado.
- A correção em `mes/services/quality.py` foi considerada de produção, não um ajuste cosmético de teste: inspeção parcial volta para a fila e evita transição inválida `fila -> finalizado` na reinspeção.
- Fixtures e testes legados foram ajustados para o teto confirmado; a cobertura incluiu um teste PostgreSQL para a regressão do Andon.
- A suíte Python completa foi executada duas vezes: **690 testes OK, 1 skipped**, de forma estável. Cadeia PostgreSQL: **8/8 OK**. Imports do produto: **12/12 OK**. Build: `tsc -b` OK e Vite com **389 módulos**.
- A validação visual existente inclui screenshots em `outputs/wave4_visual/`, incluindo `08_andon_geral.png`; a captura visual do Andon com dados PostgreSQL ficou pendente porque o preview na porta 8010 travou. O contrato funcional do Andon foi validado diretamente contra PostgreSQL TESTE.
- O estado foi documentado em `outputs/wave4_visual/ESTADO_WAVE4.md` e na memória de projeto `memory/wave4-estado-fechamento.md`.

Failures and how to do differently:

- O primeiro agente travou no preview visual da porta 8010 após concluir as alterações; o segundo agente confirmou que as edições estavam completas. Em futuras inspeções visuais, evitar subir esse preview sem uma estratégia de timeout/isolamento e não considerar um agente travado como evidência de código incompleto.
- A contagem inicial de falhas Web estava desatualizada: eram 6 falhas em 5 causas, não 5 falhas. Sempre reexecutar a suíte completa antes de editar testes.
- A suíte Python direcionada inicial não representava a situação completa; a validação final exigiu `unittest discover` completo, que encontrou e depois eliminou problemas adicionais.
- A primeira análise detectou uma possível divergência sobre refugo exceder o plano. A decisão explícita do usuário resolveu a ambiguidade: manter teto no planejado e não relaxar a migration. Não alterar uma constraint de negócio sem confirmação do usuário.

Reusable knowledge:

- `gestor_pecas_test` está em schema 25; `gestor_pecas` REAL permanece em schema 11. A verificação final do REAL foi somente leitura: schema 11, `applied_at` 2026-08-19 19:39:31, coluna da migration 25 ausente e CHECK ausente.
- A migration 25 é protegida por guardas de segurança no caminho canônico `Database()` -> `apply_migrations`: DSN de teste, nome contendo `test`, `GESTOR_EXPECTED_DATABASE` e rejeição de DSN igual ao de produção.
- A CHECK da migration 25 é `CHECK (((quantidade_boa + quantidade_refugo) <= quantidade)) NOT VALID`; a linha histórica de teste foi preservada e uma tentativa de UPDATE inválido, feita com rollback, comprovou que novas escritas são recusadas.
- O campo `sigmanest_repeat_id` pertence a `catalogo_sigmanest_planos_corte`, não a `apontamentos_corte`. O read model do Andon deve fazer JOIN por `plano_hash` e expor `repeticao`, sem levar o nome SigmaNEST ao contrato de execução.
- Pendências não bloqueantes registradas: validação visual do Andon com dados PostgreSQL; teste PostgreSQL específico para `listar_destaques_ativos_andon` (a consulta foi sondada e executou); schemas efêmeros órfãos em TESTE, não removidos por serem destrutivos; duplicação defensiva de `quality_rework_only` em `operator_flow.py` e `database.py`.
- O `.env` contém credenciais em claro; não armazenar os valores. Se o arquivo circulou, considerar rotação das credenciais.

References:

- Estado: `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes\outputs\wave4_visual\ESTADO_WAVE4.md`
- Código relevante: `app/database/database.py`, `mes/services/andon.py`, `mes/services/quality.py`, `mes/domain/manufacturing_rules.py`, `app/database/migrations.py`, `docs/REGRAS_MANUFATURA_CANONICAS.md`.
- Regressão corrigida em `app/database/database.py`, função `listar_cortes_ativos_andon`: `LEFT JOIN catalogo_sigmanest_planos_corte plano ON plano.plano_hash = corte.plano_hash` e `plano.sigmanest_repeat_id AS repeticao`.
- Visualizações: `outputs/wave4_visual/01_apontamento_dobra.png`, `02_corte_fila.png`, `03_corte_historico.png`, `04_destaque.png`, `05_solda.png`, `06_destaque_tarefa.png`, `07_qualidade.png`, `08_andon_geral.png`.

## Task 2: Promoção do banco REAL

Outcome: partial

Preference signals:

- O usuário inicialmente pediu promoção, mas aceitou explicitamente o caminho "Só após TESTE verde + backup" e depois manteve a separação "sem promoção" -> promoção deve ocorrer apenas após TESTE verde, backup restaurável, preflight e confirmação final; não executar automaticamente ao detectar que os testes passaram.

Key steps:

- Nenhum `pg_dump`, restore de validação, preflight 11->25, migration no REAL ou promoção foi executado.
- `gestor_pecas` foi repetidamente confirmado intacto em schema 11.

Failures and how to do differently:

- A promoção não pode ser considerada concluída. O próximo passo seguro é obter/confirmar a connection string de escrita, gerar backup completo do REAL, validar restauração em banco descartável, executar preflight 11->25 e parar para o OK final antes do apply.

Reusable knowledge:

- Nunca copiar dados de TESTE para REAL, executar migration no REAL ou iniciar cenário de fábrica sem autorização e sem a sequência de salvaguardas.

References:

- Banco REAL: `gestor_pecas`, schema 11, intocado.
- Banco TESTE: `gestor_pecas_test`, schema 25, validado.

