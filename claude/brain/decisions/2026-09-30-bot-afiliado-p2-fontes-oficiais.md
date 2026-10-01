# BOT AFILIADO — fontes oficiais P2

- **Status:** substituída por `2026-09-30-bot-afiliado-p3-amazon-fail-closed.md`
- **Contexto:** Amazon migrou a integração vigente para Creators API; Awin entrega Product Feed oficial; Mercado Livre documenta geração manual de links, sem API afiliada confirmada.
- **Decisão:** usar Amazon Creators API BR com OAuth e SearchItems, Awin CSV/gzip local com `aw_deep_link`, e Mercado Livre por importação assistida de link oficial. Preservar URLs afiliadas, exigir BRL e não derivar desconto de `savingBasis` ou `rrp_price`.
- **Alternativas:** PA-API 5, scraping, endpoints não documentados, conversão de moeda inventada e geração automática de link Mercado Livre foram descartados.
- **Impacto:** Awin e Mercado Livre permanecem válidos. A conclusão Amazon foi substituída após revisão das cláusulas brasileiras sobre Product Advertising Content.
