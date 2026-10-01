---
name: pull-op-protheus-401-23-09-2026
description: "23/09/2026: RESOLVIDO. Pull de OP sob demanda (VAAAC801001) devolvia HTTP 401 por senha do REST trocada no Protheus; usuário atualizou o .env e o pull voltou a funcionar (OP achada na filial 010001)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T19:45:33.270Z
---

Em 23/09/2026, ao testar a OP `VAAAC801001` (relatada pelo usuário como
existente na filial 1/matriz mas não encontrada na busca do Gestor de Peças),
implementei busca multi-filial no pull sob demanda (matriz `010001` + filial
`010004`, ver [[multi-filial-op-pull-implementado]] se existir, senão
`mes/integrations/totvs/on_demand.py`). Ao testar contra o Protheus REAL via
`scripts/homologar_totvs_op_sob_demanda_etapa62.py`, a chamada devolveu
**HTTP 401** para AS DUAS filiais — ou seja, não é problema de filial errada,
é a credencial (`GESTOR_TOTVS_OUTBOUND_USERNAME`/`PASSWORD`, reaproveitada via
interpolação no `.env` para `GESTOR_TOTVS_OP_PULL_USERNAME`/`PASSWORD`) sendo
recusada pelo Protheus nesse endpoint REST (`GESTORPECASPO`).

Isso contradiz o registro de homologação anterior (Etapa 7B, 03/09/2026, ver
`etapa7b-pull-op-homologado.md`), que confirmou pull real funcionando com essa
mesma credencial. **Causa confirmada pelo usuário em 23/09/2026: a senha do
usuário `REST` no Protheus foi trocada** — não é bug de código (verifiquei o
mecanismo de auth em `on_demand_gateway.py`: `auth=(username, password)` vira
Basic Auth padrão via `httpx`, sem transformação própria que pudesse corromper
a credencial).

**Correção:** trocar `GESTOR_TOTVS_OUTBOUND_PASSWORD` no `.env` pela senha
nova. Como `GESTOR_TOTVS_OP_PULL_PASSWORD=${GESTOR_TOTVS_OUTBOUND_PASSWORD}`
interpola dessa mesma variável, uma única edição corrige tanto o SOAP
(`WSPCP`) quanto o REST (`GESTORPECASPO`). Depois, reiniciar o backend
(`:8001`) para o `load_dotenv` recarregar o valor no boot.

**Why:** evita eu re-investigar esse 401 como se fosse bug do código do Gestor
quando reaparecer — já foi descartado (mesma falha nas duas filiais,
credencial confirmada correta localmente via `os.environ` após
`load_dotenv`, mecanismo de auth confirmado correto no código).

**How to apply:** se o pull sob demanda voltar a falhar com 401 no futuro,
perguntar primeiro se a senha do Protheus foi trocada de novo antes de
reabrir investigação de código.

**Confirmação (23/09/2026, mesmo dia):** usuário trocou
`GESTOR_TOTVS_OUTBOUND_PASSWORD` no `.env`, backend reiniciado na `:8001`,
e o script de homologação (`--branch 010001`) rodou as 11 etapas OK: OP
achada na filial matriz `010001`, produto `SPM015002001`, 1 operação
apontável (04 SECAGEM/ESTUFA). Confirma que era só credencial — nada de
código foi alterado.
