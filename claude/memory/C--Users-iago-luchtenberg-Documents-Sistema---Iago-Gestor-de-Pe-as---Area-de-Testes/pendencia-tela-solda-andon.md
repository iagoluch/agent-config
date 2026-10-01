---
name: pendencia-tela-solda-andon
description: Pendências de UI da tela de Solda e rotação de telas no Andon — IMPLEMENTADAS em 2026-09-13; uma decisão de cor (verde) fica pendente de confirmação do usuário
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-13T21:28:00.921Z
---

**STATUS: implementado em 2026-09-13** por agente em background, verificado com testes reais e no navegador contra dados reais (18 MACROs, 168 OPs). Arquivos tocados: `mes/services/welding.py` (`_agrupar_por_macro`, reaproveitando a regra A VENCER/ATRASADA/FINALIZADA já existente em `mes/domain/welding.py`), `web/src/pages/WeldingManagementPage.tsx` (seção "Acompanhamento por MACRO": rosca do total + pivot + barra 100% empilhada), `web/src/hooks/useTvRotation.ts` (já existia, alterna `/andon` ↔ `/welding-management` a cada 10s — o problema real era que nada rodava com `role === "andon"`; corrigido adicionando o perfil `sim_andon` em `simulacao/runner.py`).

**Decisão de cor resolvida em 2026-09-13.** O usuário pediu explicitamente para usar verde em "a vencer" (como no print), só que um tom diferente do verde de "finalizada". Aplicado: `--teal` (#20a7a1, verde-azulado) só na seção nova "Acompanhamento por MACRO" (rosca/tabela/barra) — o resumo do cabeçalho da tela (`.welding-summary`, widget pré-existente e não relacionado ao pedido) continua âmbar, intocado. Novo token `--teal-soft` (#e6f7f5) adicionado em `web/src/styles/tokens.css` seguindo a convenção já existente. Verificado no CSS compilado do build.

**Redesign de compactação/precisão (2026-09-13, segunda rodada de feedback):** o usuário testou no perfil `andon` (TV) e achou a tela poluída e com scrollbar. Corrigido em `web/src/pages/WeldingManagementPage.tsx` + `web/src/styles/welding.css`:
- **Modo TV**: agora mostra SÓ o pivô por MACRO (rosca + tabela + barra) — a tabela detalhada por estação e o rodapé de "leitura em" não são mais renderizados nesse modo (não faziam parte do print original e eram a causa da necessidade de rolagem). O pivô ocupa toda a altura disponível via flex (`align-items:stretch` em `.welding-macros__body`), sem scrollbar para contagens normais de MACRO.
- **Modo gerencial** (`inicio/solda`, mesma página): resumo do cabeçalho foi reduzido de 5 cartões para 2 ("OPs de conjunto soldado" e "Estações com OP") — Atrasadas/A vencer/Finalizadas saíram de lá por já aparecerem, com mais precisão (por MACRO), na rosca e na tabela logo abaixo. A tabela completa por estação continua existindo só no modo gerencial (onde rolar é aceitável).
- **Precisão de dados**: adicionada coluna "Sem prazo" na tabela do pivô (linha a linha, não só no total do rodapé como antes) — antes uma OP sem prazo aparecia como 0/0/0 sem explicação visível na linha.
- Verificado ao vivo via `tests/andon_visual_preview.py` (porta 8011, cookie `preview_perfil`) nos dois modos; teste novo `web/src/test/welding-management.test.tsx` cobrindo TV sem tabela/scroll; 20/20 testes passando; `tsc -b` limpo; build refeito.

Pedido original abaixo, mantido como referência:

Usuário reportou em 2026-09-13, observando o `/simulation-observatory` ao vivo, dois problemas na tela de Solda e no Andon que precisavam ser corrigidos numa sessão futura:

1. **Tela de Solda não está no formato desejado.** O usuário quer o acompanhamento de Solda/Andon parecido com um print que ele mostrou: uma visão tipo tabela pivot + gráficos, contando peças por `MACRO` (ex.: "SOLDADO - ACOPLAMENTO DRAPPER", "SOLDADO - PLAINA 310", etc.) cruzado com `status` (colunas: `a vencer`, `atrasado`, `finalizado`), mais um gráfico de pizza (Total: a vencer/atrasado/finalizado) e um gráfico de barras 100% empilhado por MACRO (verde = a vencer, vermelho = atrasado). O print era de uma planilha (Google Sheets/Excel) — a implementação real deve seguir **o design padrão do sistema** (Gestor de Peças), não replicar visualmente uma planilha.

2. **As duas telas gerenciais não estão rodando em rotação de 10 segundos.** Alguma tela/dashboard do sistema deveria alternar automaticamente entre duas visões gerenciais a cada 10s, e isso não está funcionando (nem durante a simulação industrial).

**Estrutura de abas pedida:**
- Dentro da aba "Tela inicial", já existe uma sub-aba "Solda" — deve ganhar mais informações (o acompanhamento descrito no item 1) em vez de ser recriada do zero.
- A sub-aba "Andon" / tela de login do Andon deve ser reservada especificamente para rodar as duas telas gerenciais alternando a cada 10 segundos (é o lugar certo para esse rodízio, não a aba Solda).

**Why:** feedback direto do usuário ao observar o dashboard ao vivo durante a simulação industrial prolongada (ver [wave6-estado](wave6-estado.md) para o estado geral do sistema nessa época). Ele foi explícito: "armazenar para nós corrigir depois" — não é para implementar nesta conversa.

**How to apply:** quando o usuário pedir para corrigir a tela de Solda ou o rodízio de telas do Andon, localizar a sub-aba Solda existente (dentro de "Tela inicial") e a tela/rota de login do Andon no frontend (`web/`), e implementar exatamente a separação de responsabilidades acima: Solda = conteúdo informativo (pivot MACRO×status + gráficos), Andon = rotação de 2 telas gerenciais a cada 10s. Confirmar com o usuário o print original se o design específico dos gráficos precisar ser revisitado.
