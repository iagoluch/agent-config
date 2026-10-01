---
name: pendencia-test-dev-observatory
description: "tests/test_dev_observatory falha em 7 testes (404) por configuração de teste, não bug de produto — ainda não corrigido"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-13T21:05:51.609Z
---

`tests/test_dev_observatory` falha em 7 testes com 404. Causa já diagnosticada (2026-09-13, achado ao validar [[dev-observatory-implementado]]): o teste monta `WebSettings(...)` sem `dev_observatory_enabled=True`, e `backend/api/main.py:505` só registra o router `dev_observatory` quando essa flag está ligada — então em teste a rota nunca existe.

**Why:** não é um bug do Dev Observatory em si (que foi verificado funcionando ao vivo, ver [[dev-observatory-implementado]]) — é a fixture do teste que não liga a flag que o próprio recurso exige por padrão (fica desligado a menos que habilitado, decisão de segurança correta). Ficou fora do escopo da tarefa que o encontrou (não pedida para corrigir).

**How to apply:** corrigir é trivial — adicionar `dev_observatory_enabled=True` na construção de `WebSettings(...)` em `tests/test_dev_observatory` (ou onde a fixture/settings do teste for montada). Não precisa investigação adicional.
