# BOT AFILIADO

## Objetivo

- FATO: construir uma operação local de afiliados que coleta por meios oficiais, normaliza, pontua, publica, rastreia cliques, importa conversões e melhora a curadoria.

## Stack

- FATO: Python 3.11+, FastAPI, SQLite, Uvicorn, Pillow, FFmpeg opcional e testes Pytest.
- DECISÃO: manter o sistema leve, sem Docker ou navegador permanente; FFmpeg é executável configurável e o fallback gera imagens/storyboards sem vídeo. LLM é opcional apenas para preview editorial.

## Arquitetura

- FATO: adapter Shopee assistido -> SQLite -> compliance -> score determinístico -> cooldown -> conteúdo Telegram -> fila persistente -> tracking -> conversões -> analytics/painel.
- DECISÃO: integração Shopee P0 é `MANUAL_OR_PENDING`; links vêm de meio oficial e permanecem intactos porque o schema autenticado brasileiro não foi verificável sem AppId/Secret.
- DECISÃO: `DRY_RUN=true` é o padrão; simulações usam estado/chave próprios e não afetam publicação, cooldown, fadiga ou métricas reais.
- DECISÃO: a fila persiste o modo e claims `dry`/`real` são isolados; circuit breaker recebe somente resultados reais; valor inválido de `DRY_RUN` falha fechado.
- FATO: P1 gera ContentPackages por canal, imagens determinísticas e MP4 vertical; `social_queue` é local e somente Reels possui preparação Graph API explícita.
- FATO: P2 seleciona adapters Shopee, Awin Product Feed e Mercado Livre manual sem alterar o modelo canônico; Amazon fica restrita ao contrato mockado.
- FATO: P3 importa CSV Admitad pelo comando `import-offers --adapter admitad` com nome de programa explícito; o import é local e não habilita ciclos nem publicação.
- DECISÃO: Admitad permanece `WAITING_FOR_REAL_EXPORT`; o adapter exige BRL e URL HTTPS da rede com SubID preservado. Distribuição e `/go` ficam bloqueados por padrão até revisão do export, programa e canal.
- DECISÃO: Magalu Influenciador, AliExpress Affiliate e SHEIN Affiliate Brasil exigem revisão antes de catálogo, fila ou `/go`; uma marca restrita no campo merchant prevalece sobre uma rede como Awin. Magalu exige link da própria vitrine, SHEIN exige link do centro de afiliados, e a documentação antiga AliExpress Affiliate API está marcada deprecated. Nenhum adapter operacional desses três foi criado sem conta e contrato vigentes.
- DECISÃO: Amazon Creators API real, import operacional, hub, `/go`, imagem e filas ficam bloqueados até aprovação escrita e desenho de retenção validado; credenciais não liberam o uso.
- DECISÃO: Awin importa CSV/gzip oficial limitado, aceita BRL e preserva `aw_deep_link`; `rrp_price` é somente referência em metadados. Mercado Livre permanece manual porque nenhuma API oficial de link afiliado foi confirmada.
- DECISÃO: `original_price` manual Shopee/Mercado Livre fica só como referência não verificada. Claims de queda/desconto exigem duas observações anteriores distintas em `price_history`, comparadas ao menor preço anterior, com prova efêmera recalculada do SQLite. O score `GOOD` começa em 45 para permitir oferta forte de preço estável sem alegar desconto. Upgrade invalida rascunhos antigos não publicados com preço riscado.
- DECISÃO: feedback de curadoria combina produto, loja, categoria, canal e hora UTC. CTR exige 20 impressões reais; CVR exige cinco cliques; EPC/receita exigem duas conversões monetárias aprovadas/pagas. Smoothing, pesos por escopo e teto agregado de ±8 evitam reação a eventos isolados.
- DECISÃO: conversão com `click_id` usa a oferta, o canal e a campanha do clique persistido; valores explícitos divergentes são recusados para evitar atribuição cruzada. `external_order_id` vazio é recusado para preservar a chave de idempotência.
- DECISÃO: Telegram espaça tentativas reais em 1,05 s; em 429 pausa o canal no SQLite pelo `retry_after` oficial sem incrementar falhas do circuit breaker e encerra o lote atual.
- DECISÃO: antes de cada envio Telegram, a fila recompõe a mensagem e revalida oferta/canal. Copy antiga ou oferta inválida é descartada sem rede, com evento `queue_rejected` atômico; um item `PROCESSING` interrompido ainda requer reconciliação humana para não duplicar envio.
- DECISÃO: resultado Telegram incerto (transporte, HTTP 5xx, resposta inválida ou falha de persistência após envio) mantém a fila em `PROCESSING`, sem retry automático. `telegram-processing` lista pendências reais e `telegram-reconcile` registra `message_id` confirmado ou descarta item cuja ausência foi verificada no canal; a escolha é humana e gera evento local `queue_reconciled`.
- DECISÃO: a fila salva a URL afiliada no enfileiramento; se ela mudar antes do envio, descarta a copy como stale e exige novo ciclo. Novas mensagens Telegram incluem `publication_key`; `/go` vincula oferta/canal/campanha/criativo à publicação real e usa a URL arquivada. Chaves simuladas/inválidas não redirecionam. Hub e mensagens legadas sem chave usam a URL atual. Compliance vigente ainda pode bloquear o redirect.
- DECISÃO: `/go` revalida a oferta no clique e retorna 410 sem gravar evento se estiver vencida, sem estoque ou com cupom expirado; o hub retira o CTA nas mesmas condições, inclusive para posts antigos vinculados por chave.
- DECISÃO: `cycle` e `scheduler-once` persistem eventos estruturados no SQLite, limitados aos 2.000 mais recentes e expostos por `app.cli events`. Eles registram estado, contagens e classe de erro, sem mensagem bruta, URL ou token; falha secundária de log não força repetição de uma publicação já concluída.
- DECISÃO: somente Instagram Reel usa Graph para `media -> status FINISHED`; Feed/Story/carrossel permanecem manuais. Token fica no header e asset URL deriva do MP4 persistido.
- DECISÃO: `media_publish` afiliado é bloqueado no código porque o contrato oficial acessível não oferece parâmetro confirmado para aplicar o rótulo de parceria paga exigido pela Meta. `#publi` e gate booleano não substituem a ferramenta; a publicação permanece manual no aplicativo oficial. TikTok afiliado com texto promocional fica `PENDING_POLICY_REVIEW`, mesmo com MP4 pronto.
- DECISÃO: o hub usa `/offers` e `/o/{slug}` sem redirect automático; somente o botão explícito chama `/go/{id}`.
- DECISÃO: Telegram integra o ContentPackage canônico com o template P0 e URL `/go`; gerar P1 não enfileira nem publica Telegram.
- FATO: P3 adiciona painel administrativo, analytics segmentado e feedback determinístico por categoria/canal/hora.
- DECISÃO: bind público exige `ADMIN_PASSWORD` e `PUBLIC_BASE_URL` HTTPS; localhost ligado em 127.0.0.1 pode operar sem senha.
- DECISÃO: CTR só existe com impressão marcada como real; feedback exige pelo menos cinco cliques, prior de vinte cliques, quarenta impressões e limite de oito pontos.
- DECISÃO: a dimensão e o feedback por hora usam UTC até existir uma regra operacional explícita de fuso local.
- DECISÃO: `OllamaProvider` local (`qwen3.5:2b`) é preferido quando disponível, seguido por `llama.cpp` configurado e template. O hook não factual validado pode entrar no ContentPackage; fatos, score, compliance, fila e publicação continuam determinísticos. `copy-preview` permanece disponível.
- DECISÃO: o worker contínuo usa lock singleton no Linux, heartbeat no SQLite, backoff e recuperação da fila P1 persistida. Inferência e FFmpeg compartilham um slot pesado entre processos da instalação.

## Decisões importantes

- DECISÃO: mensagens começam com `#publi`; publicação real exige canal cadastrado/aprovado e `PUBLIC_BASE_URL` HTTPS público aprovado.
- DECISÃO: impressões/CTR ficam indisponíveis em vez de inventados enquanto não houver fonte oficial de visualizações.
- DECISÃO: erros persistidos removem o token Telegram; segredos existem somente em variáveis de ambiente.
- DECISÃO: imagem externa só é buscada em host HTTPS oficial permitido, sem redirect e com limite de bytes/dimensões; o site não incorpora trackers externos.

## Estado atual

- FATO: repositório GitHub privado `https://github.com/iagoluch/bot-afiliado`; em 01/10/2026 a `main` local/remota foi verificada no commit `1992da0b7951f109df4cca9e8e59f17161b46f54`, com árvore limpa.
- FATO: suporte Lubuntu inclui scripts de instalação, inicialização, testes, status e instalação de units systemd para worker/web; `AGENTS.md` orienta a migração para o Acer pelo pedido "Traga o repositório para esse notebook".
- FATO: a suíte completa passou com 157 testes offline em 01/10/2026, incluindo E2E local em DRY_RUN de sample até assets, heartbeat e reabertura do SQLite. Scripts Bash e templates systemd tiveram validação estática no Windows.
- FATO: P0 a P3 local implementados em `C:\Users\iago.luchtenberg\Documents\BOT AFILIADO`.
- FATO: 9 testes Instagram passaram em 01/10/2026, cobrindo contrato de container/status, DRY_RUN, CLI, gates, segredo, vínculo do asset e bloqueio de `media_publish` sem rede ou mudança de estado.
- FATO: suíte conjunta passou com 88 testes em 01/10/2026, incluindo desconto histórico verificável, migração de rascunhos legados, feedback por CTR/CVR/EPC/receita, limites Telegram e elegibilidade de oferta forte sem desconto informado. Ciclo descartável do exemplo Shopee importou 1 oferta, enfileirou 1 item e simulou 1 publicação. Banco local `data/affiliate.db` estava vazio na revisão.
- FATO: validação direcionada da atribuição de conversões passou com 8 testes em 01/10/2026; rejeição de clique/oferta/canal divergentes e preenchimento dos campos ausentes foram comprovados em SQLite descartável.
- FATO: seis testes direcionados de compliance P3 e dois testes Awin passaram em 01/10/2026 após a revisão Magalu/AliExpress/SHEIN; oferta SHEIN inserida localmente ficou fora de hub, fila Telegram e `/go`.
- FATO: três testes de eventos operacionais passaram em 01/10/2026, incluindo comando CLI completo em DRY_RUN; sete testes de scheduler/Telegram e dez de CLI social/Admitad também passaram após a alteração.
- FATO: quatro testes de revalidação de fila passaram em 01/10/2026 para preço alterado, falta de estoque, cupom vencido e proteção de publicação já registrada; junto com P0 e limites Telegram, 28 testes passaram.
- FATO: 37 testes direcionados de Telegram, fila, P0 e eventos passaram em 01/10/2026 após proteção para entrega ambígua e reconciliação local; nenhuma chamada real à Bot API foi feita.
- FATO: 35 testes direcionados de P0/Telegram/freshness/reconciliação e 11 de migração/P1 passaram após adicionar snapshot da URL à fila.
- FATO: 50 testes direcionados P0/P1/P2/freshness/reconciliação passaram após vincular `/go` de novos posts Telegram à URL publicada; teste extra confirmou 404 para chave de simulação.
- FATO: 39 testes P0/P3 passaram após revalidar disponibilidade no redirect e no CTA; três casos novos cobrem falta de estoque, oferta vencida e cupom expirado, sem clique gravado.
- FATO: `scripts\test.bat` concluiu com 111 testes aprovados em 01/10/2026, sempre em DRY_RUN. `data/affiliate.db` permaneceu vazio (ofertas, fila, publicações, cliques e conversões com contagem zero). O usuário confirmou que ainda não possui os acessos externos necessários.
- FATO: E2E descartável passou de oferta a analytics em `DRY_RUN`, com clique 302 preservando URL/Sub_id e publicação real igual a zero.
- FATO: E2E P3 descartável gerou 6 ContentPackages, simulou Telegram, abriu 14 páginas administrativas, registrou 1 clique, manteve CTR nulo sem impressão real e `publications=0`.
- FATO: os contextos SQLite agora fecham a conexão após commit ou rollback; o E2E remove o banco temporário no Windows sem arquivo bloqueado.

## Bloqueios

- PENDENTE: aprovação no programa Shopee e dos canais de mídia.
- PENDENTE: AppId/Secret para validar o contrato oficial brasileiro.
- PENDENTE: token/chat Telegram e domínio HTTPS aprovado para teste real controlado.
- PENDENTE: export oficial real de conversões para validar o mapeamento final.
- PENDENTE: conta profissional Meta, Page vinculada, `instagram_content_publish`, token, versão Graph ativa, host HTTPS do MP4 e revisão editorial para teste Reel controlado.
- PENDENTE: contrato oficial que permita aplicar o rótulo de parceria paga via API; até existir e ser validado, publicação Instagram afiliada permanece manual.
- PENDENTE: confirmar em container real da Meta a aceitação do MP4 H.264 1080×1920/30 fps sem trilha de áudio.
- PENDENTE: app TikTok, `video.publish`, autorização/auditoria e confirmação de que o caso promocional é aceito antes de qualquer publicação via API.
- PENDENTE: instalar/configurar FFmpeg no host operacional; o binário empacotado em `.venv` foi usado somente para validação.
- PENDENTE: aprovação escrita Amazon e desenho de retenção/uso de Product Advertising Content; credenciais/Partner Tag isolados não bastam.
- PENDENTE: feed Awin real de programa aprovado para validação controlada.
- PENDENTE: export real Admitad de programa/ad space aprovados para confirmar schema, URL afiliada e regras do anunciante.
- PENDENTE: link e canal público Mercado Livre aprovados; não existe publisher nem gerador automático de link.
- PENDENTE: executar Ollama/Qwen, FFmpeg e units systemd no Acer Lubuntu real e observar desempenho e recuperação sob carga. A validação atual do Ollama foi mockada e a do systemd foi estática no Windows.
- PENDENTE: teste com binário/modelo llama.cpp real se instalado; provider remoto ainda exige contrato e política de dados. Nenhum deles bloqueia a operação determinística.

## Próximo passo

- PENDENTE: no Acer, clonar `main`, executar `bash scripts/install.sh`, instalar o modelo `qwen3.5:2b` no Ollama local, rodar `bash scripts/test.sh` e instalar as units com `bash scripts/install-systemd.sh`; conferir `bash scripts/status.sh` e logs. Não houve validação operacional no hardware alvo.
- PENDENTE: para testar o MVP real: aprovação/credenciais Shopee, token/chat e canal Telegram aprovado, domínio HTTPS público aprovado e export oficial de conversões. Awin/ML/Admitad precisam de dados/canais aprovados; Instagram/TikTok exigem suas autorizações próprias. Nenhum envio real foi executado.
