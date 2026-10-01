---
name: pente-fino-2026-09-14
description: "Auditoria geral de qualidade de código rodada em 2026-09-14 (bugs, otimização, organização, arquivos inúteis, testes) — 1 decisão de negócio pendente sobre Pintura"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-14T03:11:35.782Z
---

Relatório completo: `docs/PENTE_FINO_2026-09-14.md`.

**Corrigido de fato:**
1. Seed de homologação da Etapa 7A (`scripts/homologar_totvs_e2e_etapa7a.py:237`) quebrado desde a Wave 5 (faltava a flag `autorizador_retrabalho` exigida por coluna `NOT NULL`) — era o único erro real da suíte, corrigido.
2. `app/database/database.py:2545` (`iniciar_intervalo_automatico`) abria uma conexão do pool por recurso dentro de um laço só para checar idempotência — reduzido para 1 leitura.
3. 12 imports mortos removidos em `mes/`, `simulacao/`, `scripts/`, `tests/`.
4. 27 itens movidos para `_quarentena_revisar/` (nada apagado) — 25 arquivos de 0 byte na raiz (artefatos de shell colado errado, tipo `dict[str`, `tuple[datetime`), um `.zip` de homologação com `__pycache__` dentro, e um `.pyc` órfão.

**PENDENTE — decisão de negócio (não corrigido de propósito):** 2 testes falhando por uma causa só. A fixture real de Pintura tem 3 operações — `PINT.L` (op 40), `JATO` (op 50), `PINT.L` (op 60) — mesmo posto (`PINT.L`) aparecendo duas vezes no roteiro. O mapper projeta as 3 operações separadas; os testes esperam 4 no total só que deduplicadas. Pergunta em aberto: **uma OP que passa duas vezes pelo mesmo posto deve virar duas operações apontáveis (roteiro correto, operador aponta os dois passos) ou uma só (dedupe)?** O agente acha que deveriam ser duas (deduplicar faria o operador perder um passo de pintura), mas isso é decisão de chão de fábrica, não técnica.

**Resultados que contrariaram a hipótese inicial (bom saber):**
- `tests/` (899 testes) **não está inchado** — 0 corpos de teste idênticos entre arquivos; o único nome repetido cobre a mesma regra por duas portas diferentes (`QualityService` vs `FirstPieceService`), não é duplicata. Nada foi consolidado.
- A falha "conhecida" em `manufacturing_rules.py` (registrada em memórias antigas, ex. [[wave6-estado]]) **não existe mais** — 7/7 passando. Pode considerar esse item das memórias antigas encerrado.
- Nenhum script de `scripts/` foi para quarentena: zero-referência não prova obsolescência para CLIs chamados manualmente (ex. `run_simulacao_industrial.py` tem zero referências internas mas é a simulação ativa).

**Risco remanescente não resolvido:** `docs/` está com 120MB (61MB de evidências + 41MB de screenshots) — recomendado tirar dali, mas não executado (sem git, mover em massa milhares de arquivos referenciados por outros `.md` é arriscado de desfazer se der errado).

**Why:** pedido explícito do usuário em 2026-09-14 ("pente fino... bugs, otimizar, compactar, organização de pastas, arquivos inúteis, testes"). Rodou em paralelo com [[auditoria-seguranca-2026-09-14]] em outro agente, sem conflito de arquivos.

**How to apply:** para resolver a pendência da Pintura, decidir a regra de negócio primeiro (uma OP repetindo posto = quantas operações apontáveis?) e só then ajustar o mapper ou os testes — não corrigir só um lado sem essa decisão. Para o `_quarentena_revisar/`, é seguro revisar e apagar de vez quando quiser, nada ali é referenciado.
