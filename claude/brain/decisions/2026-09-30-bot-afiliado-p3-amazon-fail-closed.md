# BOT AFILIADO — Amazon fail closed

- **Status:** ativa
- **Contexto:** os termos brasileiros Amazon restringem agregação/análise, imagens, cache, payload, preço/estoque e redirects de Links Especiais. A persistência local atual não prova aderência.
- **Decisão:** manter apenas parser e HTTP mockado; bloquear rede padrão, CLI, import pelo pipeline, hub, `/go`, imagens e filas Amazon até aprovação escrita e desenho de retenção validado.
- **Alternativas:** liberar com credenciais, criar TTL parcial ou usar redirect `/go` foram descartadas porque não resolvem todas as cláusulas.
- **Impacto:** Amazon não é fonte operacional no P3. Credenciais e Partner Tag não alteram o bloqueio.
