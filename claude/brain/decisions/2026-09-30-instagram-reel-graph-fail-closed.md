# Instagram Reel Graph fail closed

- **Status:** ativa
- **Contexto:** a fila P1 gera Feed, Story e Reel. A Meta exige rótulo de parceria paga em post/Reel com link afiliado e comissão, mas o contrato oficial acessível de `media_publish` expõe somente `creation_id`; não foi confirmado parâmetro para aplicar o rótulo pela API.
- **Decisão:** habilitar apenas criação e consulta de container Reel. O URL público é derivado do MP4 persistido, o token fica somente no header e a aplicação não contém chamada HTTP para `media_publish`. Um booleano local não substitui o rótulo da plataforma. Publicação afiliada permanece manual no aplicativo oficial.
- **Alternativas:** confiar em `#publi`; liberar `media_publish` com gate booleano; publicar e tentar adicionar o rótulo depois; implementar Feed/Story/carrossel sem contrato oficial completo.
- **Impacto:** DRY_RUN continua sem rede; o fluxo Graph real termina em `READY_TO_PUBLISH`; Feed/Story/TikTok permanecem manuais ou pendentes. Criação de container ainda depende de host HTTPS, conta/Page/permissão e OAuth aprovados.
