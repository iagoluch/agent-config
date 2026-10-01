---
name: wave6cde-estado
description: "Waves 6C (hierarquia do Corte), 6D (Solda gerencial + ciclo TV) e 6E (filtros/humanização) — concluídas 11/09/2026, faltavam na memória anterior que só cobria 6A/6B"
metadata: 
  node_type: memory
  type: project
  originSessionId: cf9cf250-080d-46c0-be6f-81d695cbf05f
  modified: 2026-09-14T12:16:39.617Z
---

Complementa [[wave6-estado]] (que só cobria 6A/6B). Todas concluídas em `gestor_pecas_test`, REAL intocado.

**Wave 6C (11/09/2026)** — tela de Corte passou a mostrar `TAREFA → PLANO/NESTING → OP → PRODUTO` (antes era lista plana). Migration 28 adiciona `catalogo_sigmanest_ops.programa` (anulável) porque `STPIPArc.WONumber` vive na linha de peça aninhada num `ProgramName` específico — a projeção antiga descartava o programa e atribuía a OP à tarefa inteira, errado quando a tarefa tem múltiplos planos. Linhas antigas sem programa só são atribuídas automaticamente quando a tarefa tem um único plano; senão ficam em `ops_sem_plano`. Estados do plano: `AGUARDANDO CORTE`, `EM CORTE`, `DISPONÍVEL PARA DESTAQUE`, `FINALIZADO` — plano não cortado nunca aparece como pendência do Destaque. Regra "1 nesting ≠ 1 chapa" reforçada: chapas/repetição continuam vindas do SigmaNEST (`programa + chapa + RepeatID`).

**Wave 6D (11/09/2026)** — tela `/welding-management`, **gerencial** (PCP/Liderança/Supervisão/Diretoria), não operacional — nenhum login por estação criado. Linha = `(OP, operação de Solda do roteiro)`. **ESTAÇÃO é dado observado, não derivado** — decisão explícita do usuário: não existe mapeamento determinístico máquina→estação; a estação exibida é a do apontamento real, sem estação = "Estação ainda não definida.". Migration 29 cria `catalogo_pcp_ops.produto_modelo` — **mas nasce vazia, sem carga automática** (ver seção "Pendência MODELO" abaixo). Estados A VENCER/ATRASADA/FINALIZADA por regra (não estimativa): atraso nunca bloqueia fluxo. TV: `useTvRotation` alterna `/andon` → `/welding-management` → `/andon` a cada 10s, só no perfil dedicado de TV, sem alterar o Andon.

**Wave 6E (11/09/2026)** — wave de apresentação pura, nenhuma regra de negócio/API/cálculo alterada. Pausas e Crachás ganharam filtro (`RecordToolbar.tsx` compartilhado) + "Limpar filtros" persistente na sessão. Humanização centralizada em `web/src/utils/systemState.ts` (traduz `sem_registros`/`dados_insuficientes`/`nao_configurado`/`parcial`) e `web/src/utils/assistantText.ts` (remove rastro técnico das respostas da IA). Pendência de negócio não decidida: filtro por setor em Crachás não implementado porque `operadores_apontamento` não tem setor (crachá é global hoje).

## Pendência real do MODELO da Solda (cuidado: não é fato resolvido)
`catalogo_pcp_ops.produto_modelo` (migration 29) existe mas **nenhum mecanismo alimenta esse campo** — é atributo customizado do cadastro de produto no ERP corporativo e hoje não chega em nenhuma mensagem recebida pelo Gestor. Enquanto isso, a tela mostra "Modelo não identificado.". **Não inferir o modelo a partir de máquina, recurso, roteiro ou descrição do produto.** Pendência explícita de etapa futura, sem prazo.

**Why:** uma síntese externa (GPT) apresentou essa pendência como já resolvida/consolidada ("B1_ZMODELO → modelo/máquina"), o que é impreciso — o nome do campo do lado TOTVS nem está confirmado no roadmap do projeto. Registrar aqui para não repetir esse erro.

Ver também [[wave4-estado-fechamento]], [[wave6-estado]], fonte completa em `ROADMAP.md` linhas ~1790-1993.
