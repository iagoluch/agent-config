---
name: regra-recursos-apontaveis-vs-sincronizados
description: "Estado real do design de recursos de Solda: casamento é por posto físico (estação), não por processo/código de roteiro — comportamento correto, não mexer. Usuário está levantando com a Manufatura quantas estações/recursos específicos novos precisa (Solda Alumínio, Solda Aço, Ferramentaria, Robô). 2 bugs reais achados e não corrigidos, aguardando decisão."
metadata: 
  node_type: memory
  type: project
  originSessionId: cf9cf250-080d-46c0-be6f-81d695cbf05f
  modified: 2026-09-14T16:54:36.290Z
---

**ATUALIZADO 2026-09-14 — a leitura inicial estava errada, corrigida pelo próprio usuário.** Não confundir com uma tentativa anterior (mesmo dia) de restringir recursos "apontáveis" por setor — essa ideia foi abandonada pelo usuário no meio do caminho.

## Regra real, confirmada
O casamento de uma OP de Solda com um posto de trabalho é feito **pelo posto físico onde o operador está** (a estação, "Estação 1".."Estação 10"), não pelo processo/código de roteiro da OP (`D14STQ`, `SOLDA4`, etc.). Se o operador está na Estação 8 e a OP é `D14STQ`, ele faz normalmente — **o sistema não deve barrar por processo ≠ estação, e não barra hoje**. O mesmo processo pode aparecer em estações diferentes em momentos diferentes; isso é esperado, não é bug.

Confirmado por investigação de agente em 14/09/2026: "Estação 1".."Estação 10" já é uma lista curada e correta em `app/core/operator_sectors.py` (`WELDING_STATIONS`), alimentando login/grade de postos/API — não precisa recriar. Os 44 recursos com `tipo_setor='Solda'` no catálogo (`catalogo_recursos_pcfactory`) são **recursos de roteiro** (o quê fazer), ortogonais à estação (onde fazer) — as duas dimensões já são tratadas corretamente como independentes pelo sistema (`app/core/resource_mapping.py`, `sector_serves_resource()`).

## Trabalho em andamento do lado do usuário (não implementar nada ainda)
O usuário está conferindo com a Manufatura quantos recursos/estações **específicos e distintos** precisam existir além das 10 estações genéricas, porque a fábrica tem:
- **Solda de Alumínio** e **Solda de Aço** — cada uma com seus próprios boxes/estações separadas.
- **Ferramentaria** — é solda, mas é um local/recurso específico da fábrica.
- **Robô** — provavelmente já corresponde a `ROBO P` (Solda Robô Chassi Prime, 49 usos reais em roteiro) e `ROBO S` (Solda Robô Chassi S, 170 usos) dentre os 44 recursos já cadastrados — candidato natural a virar estação/recurso próprio em vez de cair numa das 10 estações genéricas.

**Não implementar nada de código para isso até o usuário trazer a lista fechada da Manufatura.**

## 2 bugs reais achados no caminho, reportados e NÃO corrigidos (aguardando decisão do usuário)

1. **Andon colapsa as 10 estações de Solda em 1 card só.** `station_resource_code()` (`app/core/resource_mapping.py:133-138`) mapeia todas as 10 estações para o mesmo código `SOLDA4`. Reproduzido isoladamente: 3 estações produzindo ao mesmo tempo → Andon mostra 1 card, os outros 2 estados são sobrescritos. **Esta é provavelmente a causa raiz do "Andon não tá visualizando algumas estações das soldas que estão rodando"** que o usuário relatou mais cedo no mesmo dia (antes se suspeitava ser efeito colateral da simulação/Codex — não era). Pintura não tem esse problema porque cada estação já tem código de catálogo próprio (`JATO`/`PREP`/`PINT.L`/`ESTUFA`/`INSPE2`).

2. **Tela de Capacidade (`GET /api/v1/analytics/capacity`) despeja o catálogo inteiro sem casar com carga real.** `listar_configuracao_capacidade_recursos()` retorna 1 linha por recurso habilitado do catálogo — 378 no TEST, das quais 309 sem `tipo_setor` (ruído puro, candidato forte ao "lixo" que o usuário via). Além disso a chave de carga está errada: linhas usam `codigo` do catálogo (`SOLDA4`), mas `by_resource`/`planned_by_resource` usam `apontamentos_operacionais.maquina` (`Estação 1`) — só coincidem por acaso (`JATO`/`Jato`), então carga/utilização fica zerada pra quase tudo. `frontend_facade.py:453-456` já resolve essa identidade via `resource_display_name()`; a Capacidade não usa isso. Não testado ponta a ponta, só leitura de código + dados.

## Implementado em 14/09/2026 (2 mudanças reais)

1. **Bug do Andon corrigido** (commit `fb2c707`): `station_resource_code()` não colapsa mais as 10 estações de Solda em `SOLDA4`; cada estação agora vira card próprio no Andon. Não mexe em elegibilidade de apontamento.
2. **Bloqueio de recurso divergente desativado para Solda** (commit `44675f3`, decisão explícita do usuário): novo `RESOURCE_CONFIRMATION_EXEMPT_SECTORS = {"solda"}` em `app/core/resource_mapping.py`, consultado no gate `confirmacao_recurso_obrigatoria` de `mes/services/operator_flow.py`. Operador na Solda não precisa mais de crachá pra apontar um recurso "divergente" do roteiro — o registro de auditoria (`setor_roteiro`/`setor_divergente`) continua gravado, só a exigência de confirmação caiu. Outros setores continuam bloqueando normalmente.

## Plano de contas de Solda em aberto (NÃO implementado, aguardando a Manufatura)
O usuário está desenhando subdivisões de recurso dentro da Solda:
- **Solda Aço**: Estação 1 a 10 (já existe, é o atual).
- **Solda Alumínio**: área física separada, quantidade de contas ainda não definida.
- **Solda Robô**: provavelmente `ROBO P`/`ROBO S` (já no catálogo, uso real 49/170 em roteiro).
- **Ferramentaria**: é solda, mas é local/recurso específico da fábrica.

Nada disso tem lista fechada ainda — não criar contas/estações novas até o usuário trazer os números da Manufatura.

## Candidatos a reclassificação dentro dos 44 (0 uso em roteiro cada, reclassificar não quebra OP nenhuma)
`ALMOXS` (Separação Almox Solda — parece almoxarifado), `MT NT` (Mont Solda Tiller — parece montagem), `SOLDA PM05` (Acabamento PM05 — parece acabamento). Usuário ainda não confirmou se são de fato áreas separadas nem para qual setor migrariam.

Ver também [[wave6cde-estado]].
