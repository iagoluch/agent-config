# Gestor de Pecas TESTE: estados de recurso e reset de OP

- FATO: `0009 — PAUSA PARA CAFE` pertence ao grupo `0002 — PARADA PROGRAMADA`.
  A leitura atual deve juntar a taxonomia de `catalogo_status_recursos`; a origem
  manual nao reclassifica esse motivo como nao planejado.
- FATO: `LASER1` (codigo de catalogo) e `Laser Ensis 3015` (nome do posto) sao
  a mesma maquina na projecao do Andon. `fila` sem OP e `Recurso sem demanda`,
  nunca fila operacional visivel.
- FATO: em `gestor_pecas_test`, `PCMITL01001` e `PCMIDN01017` foram resetadas
  somente na execucao de Dobra. Corte, catalogo, inbound TOTVS e os 16
  apontamentos de Corte finalizados vinculados permaneceram intactos.
