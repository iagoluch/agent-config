---
name: feedback-nao-remover-o-que-nao-foi-pedido
description: "Filtro/regra nova nunca pode sumir com setor, recurso ou dado que o usuário não mandou tirar (caso Destaque 25/09/2026)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f46a0007-60dd-4c1f-8944-abddd50ee087
  modified: 2026-09-25T17:12:34.961Z
---

Nunca deixar uma regra nova esconder ou remover setor, recurso ou dado que o usuário não pediu para tirar. Em 25/09/2026 o filtro "só apontáveis" tirou o Destaque do sistema. O Destaque não tem estação listada nem código de catálogo. O usuário respondeu: "isso é proibido alterar dados que eu não pedi".

**Why:** o usuário trata sumiço não pedido como violação grave, mesmo quando o dado só ficou oculto e não foi apagado.

**How to apply:**
- Antes de ligar um filtro por lista (apontáveis, catálogo, whitelist), confira no banco quais identidades têm estados/histórico hoje e compare com o que sobra depois do filtro.
- Setor sem posto listado (Destaque) usa o próprio nome como identidade.
- Quando uma migração de dados é pedida (ex.: unificar o Robô 1), faça backup em JSON (`dev_reports/`) antes de qualquer DELETE.

Ver [[calendario-etapa4b-recursos-presos-fora-turno-25-09-2026]], [[feedback-modernizacao-sem-alterar-logica]].
