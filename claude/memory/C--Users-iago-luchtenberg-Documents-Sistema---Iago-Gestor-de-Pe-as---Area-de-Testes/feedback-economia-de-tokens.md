---
name: feedback-economia-de-tokens
description: O usuário prioriza economia de tokens; evitar suítes completas e leituras de arquivos gigantes por padrão.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 11ada5d5-946c-4d91-afdd-12d961d4de56
  modified: 2026-09-10T12:24:11.519Z
---

Em 2026-09-10 o usuário pediu explicitamente para economizar tokens ("já tá em 90% de uso e nem iniciou o que eu queria"). Vale para esta e para as próximas Waves/prompts.

**Why:** o orçamento de contexto acaba antes de o trabalho principal começar quando se roda validação ampla cedo demais.

**How to apply:**
- NÃO rodar `python -m unittest discover -s tests` inteiro nem `npm test` / `npm run build` completos como rotina. Rodar só os testes do módulo/arquivo/classe diretamente afetado (ex.: `python -m unittest tests.test_quality -v`).
- `npm test`/`build` só quando o frontend for tocado, filtrando pelo arquivo de teste do componente.
- Smoke imports: só os 2-3 realmente afetados, não a lista toda do AGENTS.md.
- Preferir Grep/Glob com alvo e leitura de trechos a ler arquivos grandes inteiros.
- Ao delegar a subagentes, incluir essas restrições no prompt desde o início (não dá para redirecionar depois: SendMessage está desabilitado nesta configuração).
- Validação proporcional continua valendo — economia não é desculpa para entregar sem evidência do fluxo principal.

Relacionado: [[wave4-estado-fechamento]].
