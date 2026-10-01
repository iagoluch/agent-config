# Desconto publicável a partir de histórico

- **Status:** ativa
- **Contexto:** CSV manual Shopee/Mercado Livre traz `original_price`, mas esse campo isolado não comprova preço anterior real. A versão inicial o convertia em `discount_percent` e anunciava “De” nos canais.
- **Decisão:** guardar o valor informado somente como metadado não verificado. Anunciar queda/percentual apenas quando o SQLite tiver duas observações anteriores em timestamps distintos e o preço atual for menor que o menor preço anterior. O consumidor recebe uma visão efêmera recalculada do banco. Recalibrar `GOOD` para 50 permite publicar oferta forte sem alegar desconto. Invalidar rascunhos legados ainda não publicados.
- **Alternativas:** confiar no preço riscado do lojista; exigir desconto para toda publicação; usar um único preço anterior.
- **Impacto:** Telegram, site e criativos deixam de anunciar desconto na primeira coleta. Histórico suficiente pode habilitar a alegação posteriormente. Rascunhos legados são regenerados após upgrade; publicações já feitas permanecem como histórico.
