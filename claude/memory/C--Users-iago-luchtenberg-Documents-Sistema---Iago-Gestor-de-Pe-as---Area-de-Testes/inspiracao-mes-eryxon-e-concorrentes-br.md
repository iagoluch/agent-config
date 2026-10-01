---
name: inspiracao-mes-eryxon-e-concorrentes-br
description: "Pesquisa de 21/09/2026 sobre eryxon-flow (MES open-source europeu para job shops) e concorrentes brasileiros (SKA, Nomus) — padrões de arquitetura para inspirar o Gestor de Peças a ficar 'autônomo com IA', sem copiar literalmente."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-21T17:48:39.838Z
  originSessionId: 75e7da9f-f422-46b4-9db7-52a8b071fa8b
---

Pesquisa pedida pelo usuário em 21/09/2026 depois de gostar do eryxon-flow como referência. Objetivo: extrair PADRÕES (não código) para estruturar o Gestor de Peças de forma mais autônoma com IA. Nada disto foi implementado ainda — é inspiração para decisão futura.

## eryxon-flow (github.com/SheetMetalConnect/eryxon-flow) — o mais relevante

**"Agent-ready release" (v0.11.0) é a ideia central a copiar em espírito:**
- Regra de negócio mora em UM lugar só (lá é uma function no Postgres); UI, API REST e MCP server chamam a MESMA function — nunca reimplementam a regra em três camadas.
- Erros de regra de negócio voltam como `409 CONFLICT` com o texto da regra, não um genérico "erro 500" — dá pro agente de IA entender e decidir o que fazer.
- Um único gatilho de banco emite eventos padronizados (`job.created`, `operation.started`, etc.) — isso vira tanto o audit trail quanto o webhook para sistemas externos (no nosso caso, seria o TOTVS).
- MCP server com 113 tools, cada uma com schema de output explícito — é o mesmo princípio de contrato explícito que já usamos com FastAPI/Pydantic, só que exposto também como tools de agente, não só REST.
- Controle de acesso granular no nível de função/role (não só de rota HTTP) — reduz superfície de ataque quando um agente de IA tem uma "conta" própria no sistema.

**Outros pontos técnicos:**
- 3D viewer de STEP direto no navegador (Three.js) — evita precisar de CAD instalado para o operador ver a peça. Não é prioridade nossa hoje, mas é um diferencial de UX para chapa metálica.
- PWA responsivo mobile-first para operador, dashboard separado (QRM/WIP) para gestor — já é próximo do que já fazemos com Andon/Workbench.
- Licença Business Source License 1.1 (self-host grátis para 1 site) — modelo de negócio, não arquitetura; irrelevante pra nós que somos uso interno.

**Como isso se aplica ao Gestor de Peças:**
- Hoje `mes/domain/manufacturing_rules.py` já centraliza regra de negócio — bom, está alinhado com o padrão eryxon. Vale auditar se toda regra de transição de estado (Setup/Qualidade, gate de apontamento) realmente passa só por lá, ou se alguma tela/rota reimplica a regra localmente.
- Se algum dia expusermos um MCP server do próprio Gestor de Peças (para um agente de IA operar apontamento/OP diretamente), o modelo eryxon é o caminho: MESMO endpoint/função de domínio usado pela API REST e pelo MCP, erros de regra como resposta estruturada (não texto livre), e um log de eventos de domínio (job/operação/apontamento) que sirva tanto de auditoria quanto de gatilho para sincronizar com TOTVS.
- Vale considerar padronizar os eventos internos do sistema (ex.: `op.iniciada`, `apontamento.criado`, `qualidade.reprovada`) num único ponto de emissão, em vez de espalhados — isso facilitaria tanto auditoria quanto uma futura camada de IA que "observa" o chão de fábrica.

## Concorrentes brasileiros (SKA, Nomus) — menos técnico, mais funcional

- **SKA (SYNECO/PRODWIN)**: DNC (transmissão de programas CNC direto pra máquina) e integração com CAM (EDGECAM) — nós já temos algo equivalente via SigmaNEST para corte; vale ver se dobra/solda também merecem esse tipo de "push de programa" no futuro.
- **Nomus**: MES modular (OEE + APS + Kanban Digital) vendido em módulos que "conversam" com o ERP. Reforça que já estamos no caminho certo com Wave 6A (calendário/OEE) e o gate de Setup/Qualidade — só validar que a granularidade modular continua fácil de ligar/desligar por linha de produção.
- Nenhum dos dois BR expõe API/MCP para IA de forma pública — isso é diferencial real do eryxon-flow, não commodity no mercado nacional. Se decidirmos investir nisso, seria um diferencial competitivo, não só um "nice to have".

## Próximo passo sugerido (não decidido, só anotado)

Se o usuário quiser avançar nessa direção, o primeiro passo natural seria auditar `mes/domain/manufacturing_rules.py` e os pontos de emissão de evento existentes (Andon, operator_flow, outbox TOTVS) para ver o quão perto já estamos do padrão "uma função de domínio, múltiplos consumidores" antes de desenhar um MCP server próprio.

Ver também [[ferramentas-adotadas-auditoria-4rodadas]] e [[top12-ferramentas-21-09-2026]].
