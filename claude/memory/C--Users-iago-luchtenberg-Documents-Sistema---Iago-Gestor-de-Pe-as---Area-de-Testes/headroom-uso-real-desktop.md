---
name: headroom-uso-real-desktop
description: "Como o headroom funciona de verdade no app desktop (proxy manual, sem auto-compressão do tráfego da sessão) — decisão de 22/09/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: f960d4d6-ae46-465d-83b1-a4485978d1b2
  modified: 2026-09-22T12:04:06.758Z
---

Investigação de 22/09/2026, a pedido do usuário ("veja uma forma de conseguir usar aqui, se não conseguir, desative-o").

**Fato:** o headroom tem duas partes — um proxy HTTP local (`headroom proxy`, porta 8787, é onde a compressão de verdade acontece) e ferramentas MCP finas (`headroom_compress`/`headroom_retrieve`/`headroom_stats`) que só funcionam de verdade quando o proxy está no ar. Sem o proxy rodando, `headroom_compress` retorna `router:noop` e 0 tokens salvos.

`headroom doctor` confirma que sessões do Claude Desktop **não conseguem** rotear o próprio tráfego de API (a conversa inteira) pelo proxy — Desktop sobrescreve `ANTHROPIC_BASE_URL` e isso não é suportado (issue upstream #869). Isso é diferente do Claude Code CLI no terminal, que consegue rotear tudo automaticamente.

**Decisão:** não desativar. Iniciei o proxy manualmente em background (`nohup headroom proxy > /tmp/headroom_proxy.log 2>&1 & disown`) e confirmei via teste real (log sintético de ~540 tokens) que `headroom_compress` comprime de verdade quando chamado manualmente (28% de redução no teste, pode chegar a 90%+ em JSON/log mais repetitivo). Isso é uma forma real, ainda que manual, de "usar aqui": eu preciso lembrar de chamar `headroom_compress` antes de processar uma saída grande de Bash/Grep/log, não é automático como seria no CLI.

**Why:** o usuário pediu explicitamente para tentar fazer funcionar antes de substituir; a limitação é estrutural do Desktop (não é bug local, é limitação documentada do próprio headroom), então vale deixar registrado para não reinvestigar do zero.

**How to apply:** ao gerar/receber saída volumosa (log, JSON, dump de Bash/Grep) nesta sessão ou futuras no app desktop, considerar chamar `mcp__headroom__headroom_compress` manualmente antes de processar o conteúdo. O proxy precisa estar rodando (`headroom proxy` em background) — não há hoje um `SessionStart` hook que garanta isso automaticamente; se o proxy não estiver ativo, `headroom_compress` volta a ser no-op silencioso (verificar `headroom_stats` para confirmar `Mode: cache` e não `unknown/offline`). Ver [[ferramentas-adotadas-auditoria-4rodadas]].
