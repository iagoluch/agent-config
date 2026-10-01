---
name: repo-protheus-advpl-separado
description: "Existe um repositório separado para o código-fonte AdvPL/TLPP do Protheus, com suas próprias regras de skill routing"
metadata: 
  node_type: memory
  type: reference
  originSessionId: f83a3722-14b5-48ff-b577-fec32a3b058e
  modified: 2026-09-18T19:22:51.820Z
---

Repositório: `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Protheus-AdvPL\` (criado em 14/09/2026, ainda sem código-fonte AdvPL dentro — só CLAUDE.md/AGENTS.md e skills).

Contém `CLAUDE.md`/`AGENTS.md` com convenções específicas de AdvPL/TLPP (Hungarian notation, encoding CP-1252 obrigatório, RDMake, MVC do Protheus, SonarQube AdvPL) e `.agents/skills/` com 33 skills (mvc-generator, fwrest-client-generator, tlpp-rest-endpoint-generator, sql-code-review, advpl-to-tlpp-migration, etc. + pacote `superpowers`).

**Why:** o Gestor de Peças (este projeto) é Python/Postgres e só integra com o TOTVS via SOAP/API — não contém fonte AdvPL. As regras de CP-1252/Hungarian notation/RDMake são de um repositório diferente e nunca devem ser aplicadas aqui.

**How to apply:** se o usuário mencionar desenvolvimento AdvPL/TLPP, fontes Protheus, RDMake ou pedir para editar `.prw`/`.tlpp`, é nesse repositório separado, não neste. Se um dia o código-fonte real do Protheus for colocado lá dentro (`Fontes_Doc/Master/Fontes/`), essas regras entram em vigor automaticamente nessa pasta.

**Violação real encontrada e corrigida (18/09/2026):** as pastas `fontes/` (4 arquivos `.prw`/`.ptm`), `protheus/` e `integracao_totvs_referencia/` (XMLs reais de OP, mapeamento de campos do banco real, e uma senha real do SQL Server do TOTVS `sql_ppi`/`pcf` em texto puro) estavam versionadas dentro deste repo Python e já tinham sido publicadas no GitHub. Removidas do rastreamento e adicionadas ao `.gitignore` (ver [[gestor-pecas-github-cicd]]). A senha ficou nos commits antigos do histórico (usuário optou por não reescrever o histórico nem rotacionar a senha, por ser ambiente de homologação descartável) — reavaliar se o repositório mudar de privado para público.
