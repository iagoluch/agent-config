# BOT AFILIADO — painel e feedback local

- **Status:** ativa
- **Contexto:** o painel precisava separar operação administrativa do hub público e usar somente métricas sustentadas por eventos reais.
- **Decisão:** proteger `/`, `/admin/*` e `/api/*` com Basic em exposição HTTPS; manter localhost em 127.0.0.1 opcionalmente sem senha. CTR exige impressão real. Feedback usa volume mínimo de cinco cliques, smoothing com prior dez e ajuste limitado a oito pontos.
- **Alternativas:** painel público, CTR inferido por clique, score por um evento e modelo de ML/LLM foram descartados.
- **Impacto:** P3 funciona localmente sem nova dependência e falha fechado quando configurado para exposição insegura.
