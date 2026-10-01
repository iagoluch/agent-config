---
name: wave6-estado
description: Estado das Waves 6A (calendário/OEE) e 6B (gate Setup/Qualidade) do Gestor de Peças — concluídas e validadas em TEST
metadata: 
  node_type: memory
  type: project
  originSessionId: 8ff7d5a1-e9be-4f58-8c2d-450a35984ea2
  modified: 2026-09-11T19:15:09.957Z
---

Waves 6A e 6B concluídas e validadas em `gestor_pecas_test` (não afeta REAL).

**Wave 6A** (calendário/hora-extra/paradas/OEE): turno 08:00–17:30, fora de turno como complemento global (não duplicado por setor), hora extra via exceção `disponivel_extra` já existente, classificação central PLANEJADA/NÃO_PLANEJADA (catálogo `catalogo_status_recursos.planejado` preenchido a partir do grupo `0002 — PARADA PROGRAMADA`), OEE com fórmula intacta e entrada corrigida. Alerta de estado físico removido da apresentação (mantido internamente).

**Wave 6B** (gate Setup/Qualidade): aba "Qualidade" e card de "Primeira peça" removidos do Workbench do operador em Dobra/Usinagem/Serra; botão Setup mantido. Fluxo final:
1. Iniciar livre (sem gate) — igual Solda/Pintura.
2. Finalizar sem Setup apontado → recusado com mensagem orientando a apontar Setup (sem popup).
3. Clicar em Setup → aponta o estado E abre o popup do checklist no mesmo clique.
4. Conforme → lote liberado, popup fecha, OP retoma produção sozinha via transição `Retornar` canônica (aparece como "Retornar" comum na auditoria — decisão explícita do usuário de não criar tipo de evento distinto para retomada automática).
5. Não conforme → Retrabalho (bloqueio + crachá) ou Refugo (crachá, sem bloqueio de OP por causa da constraint `ck_primeira_peca_bloqueio` que só permite bloqueio em status RETRABALHO).
6. Depois disso, resto do lote segue apontamento único normal (um Início, um Finalizar com quantidades) — não é peça a peça como no Corte.

Inspeção dimensional (`INSPECAO`, RNC, dispensa auditável) ficou intencionalmente fora do processo do operador — backend/domínio intocado e testado, decisão de negócio documentada em AGENTS.md/ROADMAP.md (não é pendência esquecida).

Histórico de setup/checklist e autorizações por crachá (retrabalho/refugo) expostos em Análises → Qualidade (reaproveitando endpoint `/management/first-pieces` que já existia sem consumidor).

Scripts de simulação antigos (`scripts/simulacao_fabrica/`, `tests/etapa4b_factory_shift/`) foram excluídos por ficarem incompatíveis com o novo fluxo — nova versão fica para uma wave futura, ao final do projeto.

**Falha de teste pré-existente e conhecida, não é regressão**: `test_execucao_nao_conhece_a_origem_totvs` falha por causa de um comentário com a palavra "TOTVS" deixado em `mes/domain/manufacturing_rules.py` pela própria Wave 6A. Não foi corrigida por estar fora do escopo de cada wave — considerar corrigir na próxima wave que tocar esse arquivo.

**Como as waves foram executadas**: todo o trabalho de código foi delegado a um único agente `hard` em background (mesmo agente reutilizado via SendMessage para todos os ajustes/correções incrementais desta sessão, preservando contexto). Ver [[feedback-economia-de-tokens]] para a política de validação do usuário.
