---
name: auditoria-ui-total-24-09-2026
description: "Auditoria total de UI/UX de 24/09/2026 — relatório + correção em 5 ondas + fechamento 5297d6e; só Firefox/WebKit pendente."
metadata:
  node_type: memory
  type: project
  originSessionId: 7e3f4b5c-3f6b-44b8-8b53-35730e1074d1
  modified: 2026-09-25T16:25:24.547Z
---

Relatório em `docs/auditoria_ui_2026-09-24/RELATORIO.md` (1ª versão commitada em 54e2c08; revisão final oficial de 24/09 com §3.1 índice e §9 checklist, ainda não commitada); evidências e scripts Playwright reproduzíveis em `docs/evidencias/auditoria_ui_2026-09-24/` (gitignored). Snapshot em `.impeccable/critique/`.

Scores: Nielsen 20/40, técnico 11/20, Health ~53/100. 54 achados: 0 P0 · 10 P1 · 33 P2 · 11 P3. AN-01 (Andon ilegível à distância) foi reclassificado de P0 para P1 na revisão final (função funciona, falha é leitura à distância; volta a P0 só se teste na TV real mostrar cor indistinguível). OP-13: WCAG 2.5.8 AA = 24×24; 44–48px é recomendação HMI/luva, não AA.

NÃO TESTADO: Firefox/WebKit (fora do escopo por decisão do usuário, nada instalado), Dev Observatory com dados do REAL (UI coberta em instância TEST com credencial da fixture), leitor de tela real, luva/toque físico.

Efeito colateral: o clique em "Reiniciar build" (8014) reconstruiu o `web/dist` real ~13:56.

**ATUALIZAÇÃO 25/09/2026 — correção CONCLUÍDA em 5 ondas** (36e32c9, ef0cfd3, a739155, ee95754, 0e07f96, 9260cdc, 7247414) **+ fechamento 5297d6e**: GE-13 ("Sem meta definida"), IA-01 (h1/document.title de navigation.ts, incl. OperatorShell), AN-06 aceito por decisão de produto, CSS órfão removido, detector Impeccable 0 (11 supressões pontuais), fixture de chamadas sem 500. Status final em `docs/auditoria_ui_2026-09-24/CORRECOES.md` § Fechamento. Única pendência real: Firefox/WebKit (fora do escopo). Observação sem ID: 1ª carga com API lenta mostra área vazia sem indicador.

**Why:** usuário pediu auditoria sem correção; próximas sessões provavelmente vão corrigir por ordem do plano (§7 do relatório).
**How to apply:** ao corrigir UI, partir dos IDs do relatório (AN-/OP-/GE-/AX-/IA-/TE-) e respeitar [[feedback-simplicidade-chao-de-fabrica]] e [[feedback-modernizacao-sem-alterar-logica]].
