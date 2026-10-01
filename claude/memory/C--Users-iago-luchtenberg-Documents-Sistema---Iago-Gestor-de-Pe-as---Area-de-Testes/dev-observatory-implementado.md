---
name: dev-observatory-implementado
description: "Dev Observatory (logs/erros/telas/relatório por turno, TEST+REAL somente leitura) já implementado e verificado em 2026-09-13"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-13T19:45:20.942Z
---

O "Dev Observatory" pedido pelo usuário (observabilidade permanente só para o desenvolvedor, capturando logs/erros/bloqueios esperados/telas de operadores/tempo, com relatório automático por turno) foi implementado em 2026-09-13.

**Onde vive:**
- Backend: `backend/observability/` (`capture.py` — ponte com o funil de erros e o middleware; `readonly_db.py` — acesso ao REAL; `page/` — página estática do observatório) e `backend/api/routers/dev_observatory.py`.
- Rota: `/api/v1/dev-observatory` (verificado ao vivo, respondeu 200 OK com a API TEST rodando de verdade).
- Relatórios por turno: pasta `dev_reports/<data>_<turno>/report.md` (+ `report.json`), gerados automaticamente — já existem ~6 relatórios reais de turnos anteriores e do dia da implementação.
- Wiring em `backend/api/main.py`: `record_exception`/`record_response` chamados no middleware `request_context`, cobrindo inclusive 500 não previsto que escapa para o `ServerErrorMiddleware`.

**Segurança do acesso ao REAL (verificado, não só por convenção):** `backend/observability/readonly_db.py` abre a conexão com `default_transaction_read_only=on` a nível de sessão do PostgreSQL e faz uma prova de gravação (`CREATE TEMP TABLE` que deve ser recusado) logo na abertura — se a recusa não acontecer, o pool fecha e o REAL fica indisponível no observatório (falha fechada, nunca aberta). `auto_migrate=False`.

**Controle de acesso:** reaproveita a matriz de permissões existente (`app.core.permissions.can_access_dev_observatory`), nível mais restrito que o gerencial — não é um mecanismo de auth novo.

**Why:** pedido do usuário em 2026-09-13, inspirado no `/simulation-observatory` que ele viu funcionando durante a simulação industrial. Implementado por um agente `extreme` em background que foi interrompido por rate-limit da sessão, mas na prática já tinha terminado o essencial antes de cair — verificado (sintaxe, wiring, prova de leitura, rota ao vivo) numa sessão seguinte.

**How to apply:** quando o usuário pedir ajustes no Dev Observatory (mais métricas, mudar o que aparece por turno, etc.), editar diretamente esses arquivos — não precisa reimplementar do zero. [[pendencia-tela-solda-andon]] e [[pendencia-recurso-sem-demanda]] continuam pendentes, são features separadas.
