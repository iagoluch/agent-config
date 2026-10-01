---
name: feedback-ponytail-toda-tarefa
description: "Usuário pediu que a skill 'ponytail' (a base, sem sufixo) seja invocada em todos os próximos prompts deste projeto"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-22T12:19:27.746Z
---

Rodar toda a família `ponytail` em cada prompt subsequente neste projeto: `ponytail` (base, modo lazy — sempre ativa), e considerar `ponytail-review`, `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help` quando a natureza do prompt combinar com o que cada uma faz (review/audit quando houver diff ou pedido de revisão; debt quando houver comentários `ponytail:` a coletar; gain/help só quando o usuário pedir o card).

**Why:** pedido explícito do usuário em 2026-09-13 — primeiro pediu para rodar `ponytail` em todo prompt, depois pediu "execute o ponytail completo, todas skills relacionado a ele" e confirmou "nos próximos prompts" (alias para a mesma regra, aplicada a toda a família, não só à base). Em 2026-09-15 o usuário reforçou que a regra é OBRIGATÓRIA e incondicional — inclusive para mim (Claude nesta sessão) e para qualquer subagente externo (`Agent`/`Task`) que eu delegue trabalho de código, mesmo que eu "ache que não precisa".

**How to apply:** ao receber qualquer novo prompt do usuário neste projeto (Gestor de Peças — Area de Testes), invocar `Skill({skill: "ponytail"})` como parte do tratamento do prompt (rege como o código é escrito) — sempre, sem julgar se "esta tarefa é simples demais para precisar". As demais (`ponytail-review`, `ponytail-audit`, `ponytail-debt`) são one-shot por natureza — invocar quando o prompt tiver diff/revisão/débito para checar. **Delegação a subagentes:** todo prompt enviado via `Agent`/`Task` para um subagente que vá escrever/alterar código neste projeto deve incluir explicitamente a instrução para o subagente carregar e seguir a skill `ponytail` (filosofia lazy: solução mais simples, mínima, sem over-engineering) antes de implementar — não presumir que o subagente herda isso automaticamente.

**Unificado com headroom (22/09/2026):** usuário pediu para tratar a chamada do `headroom_compress` na mesma rotina de "todo prompt" do ponytail, em vez de uma regra separada — inicialmente só memória (nem o ponytail tinha `PreToolUse`, era só `description`-triggered).

**Hooks reais criados (22/09/2026):** usuário pediu explicitamente "cria o hook de verdade pros dois" após eu explicar que nenhum dos dois tinha aplicação mecânica. Implementado e testado:
- `.claude/hooks/ponytail-reminder.sh` via `UserPromptSubmit` — injeta lembrete em texto (não bloqueia) em TODO prompt do usuário, mesmo que a skill não seja lida por decisão própria.
- `.claude/hooks/headroom-remind.sh` via `PostToolUse` (matcher `Bash|Grep`) — mede o tamanho do JSON bruto de entrada do hook (`wc -c`); se > 3000 bytes, bloqueia de verdade com `{"decision":"block","reason":...}` pedindo `headroom_compress` antes de prosseguir (mesmo padrão de `typecheck-ts.sh`). Testado com saída de ~8000 bytes e confirmado o bloqueio real.
- Ambos wireados em `.claude/settings.json` e commitados (`ced1bf2`).
- Threshold ajustado para 12000 bytes (~3k tokens) em 22/09/2026 — 3000 bytes disparava até para saída moderada (git status, greps curtos), custando mais em idas-e-vindas do que economizava. Usuário pediu explicitamente "economia de tokens, porém, não te deixar burro" — ainda heurístico, pode precisar de novo ajuste com uso real.
- Ver [[feedback-auto-invocar-context7-pgaiguide-headroom]].
