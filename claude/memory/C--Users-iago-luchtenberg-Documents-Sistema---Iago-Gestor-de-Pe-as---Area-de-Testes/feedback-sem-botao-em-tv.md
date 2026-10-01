---
name: feedback-sem-botao-em-tv
description: "Telas de TV (Andon/Solda em rotação) não recebem nenhum botão, nem atalho de tela cheia"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7e3f4b5c-3f6b-44b8-8b53-35730e1074d1
  modified: 2026-09-25T12:59:21.314Z
---

As telas de Andon e Solda rodam numa TV (rotação /andon ↔ /welding-management via useTvRotation). O usuário decidiu em 25/09/2026: "não coloque botão em tv". O atalho "Tela cheia" do AN-06 foi implementado e removido por isso.

**Why:** a TV é painel de leitura à distância; qualquer controle flutuante cobre informação (o botão chegou a tampar a contagem do setor no Andon e "Estações com OP" na Solda) e ninguém interage com ela.

**How to apply:** não propor controles interativos (botões, atalhos, toggles) no modo TV do Andon/Solda; tela cheia/quiosque é configuração do navegador da TV, não da aplicação. Ver [[auditoria-ui-total-24-09-2026]] e [[feedback-simplicidade-chao-de-fabrica]].
