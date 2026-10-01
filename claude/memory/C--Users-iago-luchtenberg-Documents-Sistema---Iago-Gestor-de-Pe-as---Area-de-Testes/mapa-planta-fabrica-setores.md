---
name: mapa-planta-fabrica-setores
description: Mapeamento entre a planta baixa real da fábrica (imagem da manufatura) e os setores/nomenclatura usados no sistema — base para o futuro dashboard de piso de fábrica no Andon.
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-21T18:23:30.108Z
  originSessionId: 75e7da9f-f422-46b4-9db7-52a8b071fa8b
---

Em 21/09/2026 o usuário compartilhou a planta baixa real feita pela manufatura, pensando em usá-la como mapa visual de fundo do dashboard de piso de fábrica (ver [[analise-video-ppi-concorrente]], ponto 5, ainda vivo).

**Setores na imagem:** Estoque Chapas, Plasma, Rebarbação, Expedição, Destaque, Laser, Dobras, Usinagem, Projetos e Ferramentaria, Solda de Alumínio (aparece 2x no layout — dois blocos físicos), Serras, Estoque de Tubos, Cab. Secagem, Pintura, Jateamento, Solda de Aço, Almox, Protótipo.

**Correções de mapeamento dadas pelo usuário:**
- "Projetos e Ferramentaria" no mapa = mesma coisa (não são setores distintos, é um bloco físico único com as duas funções).
- **Robô** não aparece como bloco próprio no mapa — fisicamente fica entre Rebarbação e Expedição. Ao desenhar o mapa no sistema, representar como algo tipo "Rebarbação | Robô" (subdivisão do mesmo espaço/bloco).
- **Expedição** = mesma coisa que **Almox** (não são setores diferentes; tratar como sinônimo/mesmo local).

**Why:** necessário para bater o layout físico real contra a especificação de [[solda-5-setores-especificacao]] (Aço/Alumínio/Robô/Ferramentaria/Protótipo) e contra qualquer cadastro de setor já existente no banco, antes de desenhar o dashboard.

**How to apply:** ao construir o dashboard de piso de fábrica (ainda backlog, aguardando OK), usar esse mapeamento para não duplicar setores (Expedição/Almox, Projetos/Ferramentaria) nem esquecer o Robô como sub-bloco entre Rebarbação e Expedição.

Ver também [[analise-video-ppi-concorrente]] e [[solda-5-setores-especificacao]].
