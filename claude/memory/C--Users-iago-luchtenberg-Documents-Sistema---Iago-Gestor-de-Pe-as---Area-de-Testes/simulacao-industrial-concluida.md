---
name: simulacao-industrial-concluida
description: Simulação industrial prolongada (8h virtuais/60min reais) concluída com sucesso em 2026-09-13; onde está o relatório e o que falta
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-13T21:05:43.775Z
---

A simulação industrial prolongada pedida em `SIMULACAO_INDUSTRIAL_PROLONGADA_OBSERVABILIDADE.md` rodou até o fim com sucesso em 2026-09-13: seed 20260912, 61.8 min reais, 8.0h virtuais (8x), relatório completo em
`simulation_runs/20260913_113801/report.md` (mais eventos/erros/performance/screenshots/checkpoints na mesma pasta).

**Resultado:** 13 dos 15 critérios da seção 44 atendidos. 1 único achado ERROR do detector, 92 bloqueios esperados corretamente barrados, 0 erros 5xx/timeouts, 257 screenshots reais preservados, IA industrial respondeu 8 consultas sem vazamento técnico.

**O único achado ERROR é falso positivo, já investigado e confirmado benigno:** "Evento de apontamento gravado antes do evento anterior" com `origem_automatica=true, tipo_interrupcao=fim_turno`. Causa: `mes/services/shift_boundary.py` insere retroativamente um evento de fechamento de turno quando detecta o limite vencido (`interromper_apontamento_fim_turno`), o que pode gerar um `id` de inserção maior que o de eventos já registrados com timestamp posterior — o detector genérico de "evento fora de ordem" (`simulacao/detector.py`, verificação `evento_fora_de_ordem`) não sabe distinguir esse caso legítimo. Não é bug do Gestor.

**STATUS: as 2 pendências abaixo foram CORRIGIDAS em 2026-09-13** (mesma sessão que pediu o relatório completo). Detalhes originais mantidos como referência, com o que foi feito anexado.

1. **Contradição no relatório — CORRIGIDA.** Duas causas raiz distintas: (a) `simulacao/runner.py` filtrava paradas por `categoria = 'downtime'`, mas o valor canônico é `'parada'` (`EventCategory.DOWNTIME.value`) — o `CHECK` da tabela nem aceitava `'downtime'`, a consulta não podia retornar linha nunca; também faltava `COALESCE(s.planejado, e.planejado, FALSE)` para os 15 intervalos automáticos sem código de catálogo. (b) `simulacao/report.py` procurava chaves `"REFUGO"`/`"RETRABALHO"` maiúsculas, mas o banco grava minúsculas, e retrabalho não é evento de quantidade nessa janela (é estado) — o critério agora olha `eventos_por_estado` também.
2. **Destaque nunca completava — CORRIGIDA, bug do simulador (não do backend).** `simulacao/factory.py` filtrava planos "disponíveis" com `estado_destaque != "fim"` (incluía plano já em `'inicio'`); um plano órfão de execução anterior ficava sempre primeiro da lista → 409 `status_existente` eterno. Corrigido para selecionar só `aguardando`/`parada`.
3. **Bônus — falso positivo do detector eliminado.** `simulacao/detector.py` ganhou exclusão para `origem_automatica AND tipo_interrupcao='fim_turno'` (fechamento retroativo de turno, comportamento intencional do `shift_boundary.py`).

**Verificação real** (`simulation_runs/20260913_174049`, 2h virtuais, seed 20260912): retrabalho/refugo agora aparece (refugo 5 peças, 15 eventos), paradas planejadas/não planejadas 8/11 com pivot preenchida, Destaque completou 5 ciclos (5 início, 5 fim), achados do detector caíram de 1 (falso positivo) para 0.

**Relatório completo (não o resumo) gerado**: `simulation_runs/20260913_113801/report_completo.md` — 1854 linhas, 14 seções, cobre literalmente todos os eventos/erros/bloqueios/casos visuais/comparações de consistência sem truncar, segmentado pelos 10 checkpoints de fase.

**Ainda não corrigido (achado durante o trabalho, fora de escopo)**: `tests/test_dev_observatory` falha em 7 testes com 404 — pré-existente e independente: o teste monta `WebSettings(...)` sem `dev_observatory_enabled=True`, e `backend/api/main.py:505` só registra o router com essa flag ligada. Também no `report_completo.md` seção 12, `conteudo_em_branco` parece superestimado (210 capturas marcadas, mas com texto presente) — não investigado a fundo.
