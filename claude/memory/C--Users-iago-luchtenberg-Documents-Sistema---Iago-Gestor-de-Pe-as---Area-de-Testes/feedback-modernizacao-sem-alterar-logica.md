---
name: feedback-modernizacao-sem-alterar-logica
description: "Diretriz permanente do usuário para a auditoria/modernização de 23/09/2026 — visual pode ser redesenhado totalmente, mas lógica de negócio e dados existentes são intocáveis."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T04:26:44.324Z
---

Modernizar o visual (design "amador" atual pode e deve ser substituído por algo com cara de MES profissional) e melhorar a qualidade/robustez do backend, mas **nunca alterar informações já existentes ou a lógica de negócio presente** — só melhorar (refatorar, tornar mais robusto, mais legível), nunca mudar comportamento/resultado.

**Why:** O usuário pediu uma auditoria completa de longo prazo (23/09/2026, `/goal`) e depois explicitou que quer o sistema com "cara de MES profissional" no design, esquecendo o design que ele mesmo fez, mas fez questão de frisar duas vezes ("nunca, nunca") que a lógica e os dados existentes não podem mudar — só o código/visual em volta.

**How to apply:** Ao aplicar correções da auditoria (backend e frontend):
- Frontend/design: liberdade total para modernizar visual, layout, componentes, paleta, tipografia — não precisa preservar o design atual.
- Backend: só refatoração/hardening que preserva 100% do comportamento observável (mesmas regras, mesmos cálculos, mesmos resultados) — bugs reais que já produzem resultado ERRADO podem ser corrigidos (isso é "consertar", não "alterar lógica correta"), mas qualquer mudança que altere um resultado hoje considerado correto pelo usuário exige confirmação dele antes de aplicar.
- Na dúvida se uma mudança de backend é "correção de bug" vs "alteração de lógica", tratar como alteração de lógica e perguntar antes.
