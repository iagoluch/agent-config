v1

## User Profile

O usuário trabalha intensivamente no MES Gestor de Peças em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes` e também em `C:\Users\iago.luchtenberg\Documents\iago-company-os`, incluindo FastAPI/React Web, Python/PySide6 legado, PostgreSQL, simulação fabril, TOTVS/Protheus e validação controlada de providers. Espera trabalho direto e baseado em evidência: inspecionar antes, fazer mudanças estreitas, preservar limites TESTE/REAL e efeitos externos, e distinguir FATO, DECISÃO, HIPÓTESE, PENDENTE e INFERÊNCIA. Valoriza fluxos de operador simples e visuais aprovados/familiares; Git/GitHub faz parte do fluxo. Quando solicitado, responder em português. [ad-hoc note]

## User preferences

- For visual audits, "Nao faca correcoes. Nao analise o design. Apenas gere o relatorio visual completo." -> deliver standalone capture/documentation only; use safe read-only states and exclude messages, payments, spending, deletions, external actions, and real authorizations.

- Em extração web/ERP, “procure formas fáceis de exportar para economizar tokens” e “se atente à economia de token” -> coletar dados estruturais compactos, em lote e sem despejar árvores AX/screenshots; para “TODOS os caminhos”, declarar cobertura e lacunas explicitamente.

- Para OEE enviado à Manufatura, separar regra vigente, fontes, exclusões, ausência de dados e pendências de homologação.
- Em segurança, testes agressivos são autorizados somente no TESTE local, sem produção/REAL; entregue comandos completos prontos para colar e valide achados automáticos contra API/código antes de corrigir.
- Mantenha escopo estrito quando o usuário pedir para não gastar tokens com explicações prematuras; não faça trabalho paralelo.
- Commit exige pedido explícito; push também exige autorização explícita. Para uma frente isolada, use `git commit -- <paths>` e preserve WIP.

- Prefira soluções simples e diretamente aplicáveis; para trabalho localizado, evite análise global e suíte completa, usando validação dirigida e proporcional ao risco.
- Para um ensaio isolado, “pode fazer bem fajuto a VM” -> use a configuração mínima funcional; não aplique sizing de produção sem necessidade.
- Em pedidos “rápidos” ou “de forma rápida”, execute diretamente e só declare sucesso após uma validação objetiva do artefato/resultado.
- “Oque der de você fazer, faça ja ... e me explique de forma simples depois” -> conclua toda implementação/validação segura e deixe apenas login, credenciais, pagamento ou decisão de conta para o usuário, em passos curtos.
- Após “não entendi” diante de shell multi-etapa, dê um comando por vez ou um helper único; não volte a recomendar pagar/ativar um provider explicitamente adiado, como Apollo.
- Para “um comando do cmd”, entregue primeiro uma única linha copiável para CMD; se houver fallback, mantenha explícito quando a execução não foi confirmada.
- Não delegue/suba subagentes sem pedido explícito: “esses agentes vão acabar com o meu uso”. Em auditorias, só finalize quando estiver “seguro” e entregue “um contexto de TUDO” factual, preservando WIP.
- Para auditoria diagnóstica, “NÃO corrija código” e “Somente TEST; nunca tocar/escrever no REAL”: registre HEAD/status e documentos-base, evidencie ou marque não testado cada área, e preserve WIP de outras sessões.
- No `iago-company-os`, comece por `AGENTS.md` e `company/AI_OPERATING_RULES.md`; preserve modular-monolith/PostgreSQL e pare para decisão CEO quando a arquitetura for genuinamente nova.
- Para receita, complete a preparação interna segura, mas não faça outreach/efeito externo sem autorização explícita; `READY_FOR_OUTREACH` não é receita realizada.
- Antes de ações destrutivas, REAL ou integrações externas, prove o alvo efetivo; em reset TESTE, mostre dry-run/listas/contagens e exija confirmação literal.
- Em pedido explícito do desenvolvedor para TESTE, pode executar o reset pontual sem criar feature de reabertura; ainda confirme banco/tabelas/contagens e preserve o escopo.
- Para commits, confira status, instruções, histórico e diff; agrupe somente mudanças coerentes e validadas, preservando WIP não relacionado.
- Depois que o alvo de uma ação destrutiva já estiver comprovado, “Apenas formate, sem objeção ... não enrole.” -> execute diretamente e comunique objetivamente; a confirmação inicial do alvo continua obrigatória.
- Para entregáveis de automação, “não quero código solto” -> crie, teste, empacote e devolva os caminhos dos artefatos; valide ZIP por tamanho não zero e enumeração do conteúdo.
- “Tudo que está modificado” + “Push direto na master” é autorização específica, não padrão: ao ocorrer, ainda faça varredura de secrets, confira branch/remoto e valide o working tree final.
- Para fluxos MES de operador, “o sistema tem que ser do mais simples possível”; não acrescente gates, leituras obrigatórias, fotos ou checklist por padrão.
- Para mockup “mas não faça coding ainda”, altere só o mockup. Em visual, use `Designs aprovados/Telas` e `Designs aprovados/Icons`, sem estética não aprovada. [ad-hoc note]
- Em motion graphics de produto, “Faça do meu projeto” e “Tente seguir o design do sistema” -> começar por tokens, logo e capturas reais; não usar estética genérica desconectada da UI.
- Ao sincronizar Claude/Codex após “puxe os hooks recentes do claude” / “se atualize”, reaudite a configuração viva e mantenha infraestrutura de agente separada do produto.
- Para mudanças Claude→Goose, “não reconstruir o Goose”, “nunca expor secrets” e “não limitar o Claude” -> mantenha Claude como fonte de verdade e use adapters incrementais com backup, dry-run, rollback e validação de schema.
- Quando o objetivo for “utilizar mais” llm-council, empresa de agentes e skills úteis, consulte o mapa de skills em tarefa R1+ e delegue só trabalho realmente independente; hook/roteamento não é prova de council executado.
- Em instalação de skill, “torne isso automático, não quero escrever pra ativar” -> preferir acionamento semântico para decisões/trade-offs reais; não exigir frase-chave.
- Para um patch de configuração localizado, “confirme o que foi escrito e não altere mais nada no arquivo” -> preservar o conteúdo fora do alvo e reler exatamente a seção editada.
- “muda o modelo padrão que eu uso para opus 5.5 high”; o `standard` também deve usar Opus. Ao verificar, confira `settings.json` e o frontmatter do subagente, pois o `effort` pode divergir.
- Em auditoria UI/UX, “NÃO corrija código” e “NÃO PULAR”: use `/impeccable critique` antes de `audit`/`detector`, esgote alternativas antes de `NÃO TESTADO` e entregue evidência por achado.
- Quando corrigir UI/UX por ondas, faça análise individual, mantenha pt-BR e rastreabilidade por ID, e não altere OEE, lógica MES ou dados. Andon/Solda são TV: “não coloque botão em tv”.
- Para a Consulta Operacional, “foque na regra ... sobre quais recursos são usados”: use `OPERATOR_SECTORS`/postos apontáveis, não histórico incidental ou o catálogo sincronizado inteiro.

## General Tips

- In standalone visual HTML, `loading="lazy"` images can look broken before decoding; force `loading='eager'` and await `decode()` before concluding. Run Playwright from `web` when that directory owns its dependencies.

- Oriente-se por `AGENTS.md` → `ROADMAP.md` → `docs/STATUS_ATUAL.md` → Git status/log; `STATUS_ATUAL.md` é a fonte operacional mais recente e WIP deve ser preservado. [ad-hoc note]
- Em `:8001`, a UI vem de `web/dist`, não HMR: após front-end, build, reinicie TESTE quando aplicável, health-check, hard-refresh e valide o artefato servido. [ad-hoc note]
- Antes de diagnosticar estado ou contagem em `:8001`, confirme o banco efetivo do processo (`TEST_DATABASE_URL` para `gestor_pecas_test`) e descarte listener antigo sem reload.
- Antes de editar CSS, procure todos os overrides responsivos; antes de trocar asset, trace import e ponto de uso.
- Rode comandos backend da raiz, use guards TEST-only e prove `current_database()` antes de alterar dados. Migração nova requer `SCHEMA_VERSION`, restart sem reload e verificação de schema TESTE.
- Em segurança/integração industrial, não inferir contrato TOTVS de payload ambíguo. F18 não autoriza desativar OP por `StatusOrderType`/snapshot sem contrato oficial.
- Para auditoria ampla, trabalhar em um agente coerente e revalidar achados no código; o usuário rejeitou agentes em massa e conclusão sem prova requisito a requisito.
- Nunca armazene segredos. Listener ou handshake MCP não prova operação; valide o fluxo seguro subsequente.
- Em Telegram, HTTP 200 não basta: confirme JSON `ok=true`; notificações devem ficar fora da transação que persiste o evento industrial.
- Brain compartilhado: em caminho Windows acentuado, `Peças` → `PeÃ§as` pode invalidar `cwd` e mascarar Git; garantir UTF-8 e preservar diagnósticos antes de concluir que Git falhou.
- No launcher local atual, `python reiniciar_build.py` compila Web antes de reiniciar 8001; depois confirme health, banco TESTE, schema e simulação desligada.
- Em sincronização Goose, `sync_lock()` previne a corrida watcher/sync manual; após editar o script reinicie o watcher. Valide Goose Desktop e `goose run` separadamente: o CLI não executa hooks de plugin, embora carregue skills e suporte `delegate`.
- Em OpenCode 2.x, valide Desktop e CLI separadamente: plugins compatíveis usam `export default { id, setup, server }`; logs/instrumentação, não a fala do Nemotron, comprovam hooks. Sob MSIX, use uv tools fora de AppData e não considere `memoria_salvar`/Headroom prontos até o teste Desktop confirmar `execute`/`mcp connected`.
- Em terminais Windows abrindo em sequência, siga a cadeia temporal e pai/filho; um burst `com.docker.backend.exe` → `wsl.exe` → `wslhost.exe`/`conhost.exe` é evidência forte de Docker/WSL, não prova de janela visível. Para concluir, habilite auditoria 4688 com linha de comando na próxima ocorrência.
- Em validação de providers no `iago-company-os`, use evidência sanitizada em arquivo com `record_provider_validation.py --evidence-file ... --execute`, banco isolado e replays do mesmo evento para idempotência; nunca registre segredos ou ative o provider apenas para validar.
- No `iago-company-os`, `scripts/validate_repository.py` é a porta inicial; trate resultados, serviços locais, IDs e commits históricos como snapshots e revalide o estado atual.

## What's in Memory

### C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

#### 2026-09-30

- VM de teste VirtualBox e reinstalação Windows Server: `Gestor-Pecas-VM`, `VBoxManage.exe`, `Windows Server 2025`, `unattended install`, `VMState="running"`, `instalar_vm.ps1`
  - desc: Formatação confirmada e reinstalação iniciada da VM TESTE; consulte antes de retomar pós-instalação ou executar manutenção destrutiva da VM neste host.
  - learnings: `VMState="running"` não basta: em VirtualBox sobre Hyper-V, `VideoMode="0,0,0"`/screenshot `0x0` pediu BIOS sem TPM; login, término da instalação e prontidão continuam não validados.
- Strix, autenticação e unicidade das pausas: `Strix`, `session_version`, `INSERT ... ON CONFLICT ... RETURNING`, `uq_pausa_setor_ordem`, `PauseOrderConflictError`, `HTTP 409`
  - desc: Auditoria local TESTE e fixes de auth; consulte antes de interpretar scanner, alterar logout/throttle ou retomar a migration 54 de ordem das pausas.
  - learnings: Confirme o contrato `username`/`password` e o contexto de domínio antes de aceitar IDOR/XSS; logout/throttle foram testados, mas migration 54 ainda exige aplicação TEST, concorrência e 409 comprovados.
- Migration 53, instalador VM e auditoria backend: `migration 53`, `1303`, `DOBRA3`, `deploy/instalar.ps1`, `backup_diario.ps1`, `1324 passed, 1 failed, 1 skipped`
  - desc: Saneamento já aplicado em REAL, ensaio do instalador e evidência de auditoria; consulte antes de nova migration, pacote/deploy ou conclusão de capacidade backend.
  - learnings: Migration 53 é histórica e não pode ser editada; o ensaio VM funcionou, mas VM limpa e testes REAL de volume/outage/rollback continuam não verificados.

### C:\Users\iago.luchtenberg\AppData\Roaming\Claude\scratch-workspaces\3b9c2856-223a-4112-aa9a-9b9de00331d6\94900231-2415-49d7-9bb6-2ce48172cbea\scratch-2026-09-30-aed621

#### 2026-09-30

- Windows Sandbox PowerShell test harness: `Windows Sandbox`, `.wsb`, `sandbox/launch.ps1`, `sandbox/guest/run.ps1`, `WDAGUtilityAccount`, `Containers-DisposableClientVM`, `result.json`
  - desc: Harness host/guest para cópia sanitizada e testes descartáveis; consultar antes de recriar o fluxo em outro repositório ou alegar isolamento real.
  - learnings: A cópia exclui segredos e os scripts validaram dry-run/códigos reservados; use caminho curto, BOM UTF-8 no PowerShell 5.1 e habilite/reinicie o Sandbox antes do primeiro boot fim a fim.
- Diagnóstico de terminais sequenciais Docker/WSL: `Docker Desktop`, `com.docker.backend.exe`, `wsl.exe`, `wslhost.exe`, `conhost.exe`, `event 4688`, `CREATE_NO_WINDOW`
  - desc: Diagnóstico parcial da rajada de consoles neste host/scratch cwd; consulte para investigar abertura sequencial sem confundir a hipótese Goose com a árvore de processos observada.
  - learnings: Docker/WSL é a explicação líder, mas cada `conhost.exe` não foi confirmado como janela visível; correlacione pais e linha de comando no próximo evento.

### C:\Users\iago.luchtenberg\Documents\Codex\2026-09-29\use-este-prompt-no-codex-da

#### 2026-09-29

- TOTVS Protheus crawler/documenter somente leitura: `Playwright`, `CDP`, `Shadow DOM`, `wa-webview`, `BFS`, `skipped-actions.json`, `verify-export.js`, `totvs-crawler.zip`
  - desc: Crawler Windows pronto e validado para uma aba autenticada Protheus; procure antes de construir/exportar documentação offline com navegação fail-closed neste cwd.
  - learnings: Menus são componentes Shadow DOM e podem aninhar iframe; percorra árvore composta/frames, valide ZIP por abertura/entradas e declare captura parcial se rotinas de negócio permanecerem fora do escopo.

### C:\Users\iago.luchtenberg\Documents\Codex\2026-09-29\ex

#### 2026-09-29

- TOTVS Protheus Web Agent route/catalog extraction: `Web Agent`, `cua_repl`, `DOM snapshot`, `COMP3071`, `COMP3092`, `no_visible_match`, `Planej.Contr. Produção`
  - desc: Navegação autenticada e somente leitura para mapear rotas/routines no Protheus; consulte antes de exportar HTML ou declarar cobertura completa neste cwd.
  - learnings: Web Agent suporta DOM/AX estrutural, mas IDs dinâmicos exigem estado novo por interação; o rollout é parcial e não produziu HTML nem verificação fim a fim.

### C:\Users\iago.luchtenberg\Documents\iago-company-os

#### 2026-09-28

- Playwright visual audit as standalone HTML: `ui-audit-report.html`, `data:image`, `loading='eager'`, `decode()`, `lightbox`, `manifest`, `IAgo Control Center`
  - desc: Read-only capture of Empresa/Trabalho/Negocio/Decisoes/Sistema in `cwd=C:\Users\iago.luchtenberg\Documents\iago-company-os`; search before generating visual documentation without UI fixes.
  - learnings: The artifact validated 152 captures/manifest, `broken=0`, `external=0`, filters and lightbox; explicitly decode lazy images and run Playwright in `web`.

#### 2026-09-27

- Fase 1 e primeiro checkpoint de receita: `AGENTS.md`, `company/AI_OPERATING_RULES.md`, `WORKFLOW_POLICY.yaml`, `FOR UPDATE SKIP LOCKED`, `READY_FOR_OUTREACH`, `docs/FIRST_REAL_REVENUE_VALIDATION.md`
  - desc: Core PostgreSQL determinístico e validação operacional do primeiro RevenueRun; procure antes de evoluir arquitetura/runtime ou retomar a mão-off comercial em `cwd=C:\Users\iago.luchtenberg\Documents\iago-company-os`.
  - learnings: ModelRouter é apenas configuração; lease/heartbeat/idempotência são persistentes; `READY_FOR_OUTREACH` exige contato externo, Deal WON, pagamento observado e decisão CEO antes de chamar receita.
- Provider readiness, ledger and controlled smokes: `record_provider_validation.py`, `--evidence-file`, `iago_smoke`, `Stripe`, `Tavily`, `Apollo`, `stripe events resend`
  - desc: Validação operacional sem ativação/segredos; procure primeiro para registrar evidência, reproduzir idempotência em provider ou entender o estado Stripe/Tavily/Apollo/Claude.
  - learnings: Use arquivo de evidência no PowerShell 5.1; Stripe e Tavily estão validados, Apollo permanece `FAILED`/deferred por HTTP 403 de entitlement, e Claude login está pendente.
- Latest commit hardening review: `3341a769a3b98f5edb861ed4629e40e6d1ed3da1`, `provider-smoke.yml`, `workflow_dispatch`, `EconomicGovernanceService`, `x-api-key`
  - desc: Revisão do `HEAD` de hardening de providers/governança; consulte antes de alterar workflow de smoke, sanitização de evidência ou regra de decisão CEO.
  - learnings: Inputs de workflow usam `env`, governança exige `ceo`, e a checagem de `${{ inputs.` ainda é específica a `provider-smoke.yml`; o rollout não executou testes.

### C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

#### 2026-09-29

- Sincronização Claude→Goose, Superpowers e workforce: `claude-goose-sync`, `sync_lock`, `Goose 1.52.0`, `superpowers@claude-plugins-official`, `CLAUDE_PLUGIN_ROOT`, `delegate`, `llm-council`
  - desc: Paridade Claude-fonte-de-verdade com Goose/Nemotron, lock de sync, hooks/plugins e validação de workforce; consulte antes de editar `~/.claude-goose-sync` ou afirmar que uma capability roda no Desktop/CLI.
  - learnings: Quatro syncs concorrentes passaram com lock e `0 drift`; Desktop executa hooks de plugin, CLI não. `delegate` foi validado, mas council completo continua pendente de uma decisão real.

#### 2026-09-28

- Exportação Claude Code → OpenCode/Nemotron, memória inbox e MCPs: `OpenCode 2.0.18`, `CLI 1.18.14`, `export default`, `setup`, `server`, `memoria_salvar`, `UV_TOOL_DIR`, `uv trampoline failed to canonicalize script path`
  - desc: Compatibilidade de plugins, inbox compartilhada e runtime Headroom/graphify no Desktop OpenCode; procure antes de editar `.opencode/`, `scripts/export_opencode.py` ou diagnosticar MSIX.
  - learnings: O formato duplo carregou e injetou hooks; `memoria_salvar` ainda deu `Unknown tool` no Desktop e a reconexão Headroom ainda exige prova por log `mcp connected server=headroom`.
- Showreel motion graphics do Gestor de Peças: `showreel`, `motion-graphics`, `design-system`, `tokens.css`, `andon.css`, `logo_gestor_pecas.png`, `canvas`, `Playwright`, `imageio-ffmpeg`, `xstack`
  - desc: Vídeo de 15 s criado para o produto real neste cwd; procure antes de produzir outro showreel, reutilizar o pipeline de canvas/frames/ffmpeg ou decidir estética de motion.
  - learnings: Começar por tokens/logo/capturas reais; o resultado validado é H.264/AAC 1920×1080 60 fps. Para preview de um único frame, não use `xstack`; valide PNG direto e estados de texto longo.
- TEST backend/MES diagnostic audit: `backend-audit`, `PGPOOL_MAX_SIZE=4`, `/andon`, `EXPLAIN`, `gestor_pecas_test_audit_bench`, `RELATORIO.md`
  - desc: P0-P3 evidence and TEST-only boundary for resuming backend/MES audit; search this current diagnostic evidence before any backend/MES audit.
  - learnings: P0-01 reproduced pool exhaustion (5 of 6 366-day `/andon` returned 503); the 245,500-appointment benchmark was disposable/synthetic, and Git cleanup remains pending.
- Recursos contínuos, aliases e retorno de pausa: `listar_recursos_ativos_scheduler`, `resolve_resource_identity`, `INSPE2`, `PREP`, `finalizar_intervalo_automatico`, `iniciar_sistema_teste_cloudflare.py`
  - desc: Evidência atualizada da implementação parcial de recursos habilitados, calendário global e restauração após pausa no checkout TESTE; consulte antes de depurar cards-aliás ou estado contínuo.
  - learnings: Corrija a projeção pela identidade canônica, restaure o snapshot completo ao fim da pausa e não declare aplicação no TESTE antes de reiniciar o Uvicorn real e verificar health/schema/ciclo do scheduler. A regra de OEE deste rollout foi substituída pela corporativa de 2026-09-25.

#### 2026-09-26

- Auditoria backend/MES e commit pendente, não executados: `backend-audit`, `AGENTS.md`, `ROADMAP.md`, `STATUS_ATUAL.md`, `git status`, `docs/auditoria_backend_2026-09-25/RELATORIO.md`
  - desc: Handoff TEST-only para retomar auditoria diagnóstica e um commit solicitado, sem misturar alterações de outras sessões.
  - learnings: A sessão encerrou antes de qualquer inspeção, teste, relatório ou commit; todo resultado permanece pendente.

#### 2026-09-25

- Instagram saved Reels, Claude/Codex e relatório: `Instagram`, `saved-posts`, `Context7`, `Task Observer`, `MCP`, `outputs/relatorio-reels-ia-claude-codex.md`
  - desc: Pesquisa de ferramentas a partir de Reels salvos e comparação com a infraestrutura local; consulte para triagem/adoção sem instalar por impulso.
  - learnings: Instagram é descoberta, não prova; use lotes curtos por virtualização e valide repositórios/ativação. Recomenda Context7, uma rota OpenAI Docs e prova de OmniRoute antes de pacotes sobrepostos.

- Recursos apontáveis, Fora Turno e Consulta Operacional: `ETAPA4B_TESTE_20260831`, `TEST_DATABASE_URL`, `OPERATOR_SECTORS`, `is_apontavel_resource`, `shared_post_name`, `station_resource_code`
  - desc: Correção TEST de calendário residual e projeção de cards apontáveis; procure primeiro para recursos presos em `fora_turno`, duplicidade Robô 1/ESTUFA ou filtro de operações.
  - learnings: 75 vínculos residuais foram removidos só no TEST; `/operations/overview`, `/resources` e `/stream` usam regra central e preservam recurso com execução, OP ou conta ativa. Processo 8001 sem reload pode mascarar a correção.
- Auditoria UI/UX Onda 4/5: `9260cdc`, `matrix.py`, `h1.visually-hidden`, `contar_chamadas_nao_vistas`, `Dev-Observatory`, `web/dist`
  - desc: Onda 4 publicada e regressão responsiva Onda 5 ainda parcial; procure para correção/auditoria por ID, TV Andon/Solda e fechamento de matriz visual.
  - learnings: Onda 4 teve build/tsc e testes dirigidos verdes; Onda 5 reduziu métricas em 430 pares, mas ainda precisa documentação, fechamento e commit. Fixture 500 e título oculto não são regressões reais.

#### 2026-09-24

- OEE corporativo, timeline e pausas: `calculate_oee`, `REGRA_CORPORATIVA_SEM_DEMANDA`, `parametros_turno`, `H1`, `H2`, `intervalo_programado`, `ad8410a`
  - desc: Regra corporativa e timeline contínua por recurso; procure para OEE/sem demanda no checkout TESTE, após conferir o estado mais novo de recurso em 2026-09-25.
  - learnings: Em período misto, `sem_demanda` sai das bases; se integral, A=100%, P=0%, FTT indisponível e OEE=0%. H1/H2 são configuráveis, não hardcoded.
- Configuração Claude Opus 5.5 e subagente standard: `claude-opus-5-5`, `effortLevel`, `settings.json`, `standard.md`, `model: opus`
  - desc: Preferência global de modelo Claude, aplicável além deste checkout; consulte ao verificar/defaultar sessões ou subagentes.
  - learnings: Global está em high, mas `standard.md` fixa Opus medium; configuração de projeto pode sobrescrever a global.
- Especificação de auditoria total de design UI/UX: `/impeccable critique`, `Playwright`, `WCAG 2.2 AA`, `evidence-matrix`, `NÃO TESTADO`
  - desc: Pedido anterior de auditoria sem código; consulte para preservar o método e a fronteira quando a autorização atual não incluir correções.
  - learnings: Não confundir este pedido sem execução com a posterior Onda 4/5; a matriz deve cobrir áreas/fluxos/estados, resoluções e zooms, com evidência por achado.
#### 2026-09-23

- Auditoria F1–F21, fail-closed e backup TESTE: `F1-F21`, `GESTOR_TOTVS_SOAP_ALLOWED_SOURCE_CIDRS`, `readonly_db.py`, `backup_banco_teste.py`, `F18`, `76c2cac`
  - desc: Auditoria parcial, SOAP por peer TCP, Dev Observatory read-only e backup PostgreSQL verificável; consulte antes de declarar pronto/usar REAL.
  - learnings: `:8001` pode estar com código antigo; faltam CIDR Protheus, role SELECT, contrato F18 e restore/DR operacional.
- Reset pontual de OPs e cotas de primeira peça: `PCMITL01001`, `PCMIDN01017`, `PCMD8201001`, `apontamentos_operacionais`, `qualidade_primeira_peca`, `ForeignKeyViolation`
  - desc: Reset autorizado de três OPs Dobra no `gestor_pecas_test`; consulte para restaurar execução/primeira peça sem reabrir fluxo como feature.
  - learnings: Estado inicial é `Aguardando`/`PENDENTE`; `codigo_status_recurso=0` viola FK — usar `NULL` salvo código válido.
- Pausas padrão, limpeza e publicação: `migration 43`, `SCHEMA_VERSION 43`, `_garantir_pausas_padrao`, `tests/helpers.py`, `verificar_groq_*`, `cb87579`
  - desc: Provisionamento de pausas de Solda, limpeza estrutural e publicação autorizada na `master`.
  - learnings: Migration só roda com `SCHEMA_VERSION`; antes de excluir scripts confirme dependências reais; `cb87579` é histórico, não pressuposto de Git atual.
- React Web sidebar, PageFrame e OperatorShell: `AppShell`, `OperatorShell`, `PageFrame`, `assets.profile`, `icone_perfil.png`, `web/dist`
  - desc: Refinamento visual e commit seguro do header/operator no checkout TESTE.
  - learnings: Trace asset real, cubra overrides CSS e valide o bundle compilado servido.
- Commit pending operator-header WIP: `3f3e369`, `git status`, `docs/STATUS_ATUAL.md`, `hook push`, `44 testes Web`
  - desc: Checklist de consolidação de WIP Web coerente.
  - learnings: Hooks podem fazer push em `master`; conferir branch/remotes após commit.
- Infraestrutura Claude→Codex, hooks, skills e MCPs: `.codex/hooks.json`, `Impeccable`, `composio-automation-catalog`, `headroom.exe`, `pg-aiguide`, `Unknown Mcp-Session-Id header`
  - desc: Paridade operacional parcial sem alterar produto; use para Git Bash no PowerShell, skills Composio sob demanda e validação MCP.
  - learnings: OmniRoute só teve handshake; requer session ID + `notifications/initialized` + `tools/list` antes de ser funcional.

#### 2026-09-22

- Auto-compactação e hooks Claude: `autoCompactWindow`, `200000`, `headroom_compress`, `127.0.0.1:8787`, `ponytail-reminder.sh`
  - desc: Configuração de contexto e manutenção histórica de hooks/MCP Claude.
  - learnings: Nova sessão pode ser necessária; `router:noop` não é prova de compressão.
- Primeira peça, Retrabalho, reset de OP e Paradas & Setup: `WorkbenchPage.tsx`, `SetupQualityDialog`, `reiniciar_ops_teste.py`, `--incluir-templates`
  - desc: UI e reset TESTE com confirmação/dry-run.
  - learnings: Inspecionar `currentStatus`/`firstPiece` e bundle servido antes de afirmar correção.
- Crash Histórico → Fila e ErrorBoundary: `operationLabel`, `useApiQuery`, `findIndex=-1`, `OperatorPortalPage.tsx`
  - desc: Correção de troca de OP concluída para fila operacional.
  - learnings: Dados de seleção podem estar stale; mantenha shell fora de ErrorBoundary operacional.

### Older Memory Topics

#### Gestor de Peças TESTE checkout

- Segurança, simulação, qualidade, observabilidade e ondas MES: `gestor_pecas_test`, `current_database()`, `Wave 4`, `Wave 5.1`, `Wave 6A`, `Quality`, `Dev Observatory`
  - desc: Runbooks TEST-only, simulação industrial, validações de qualidade/segurança e handoffs; cwd=Gestor de Peças TESTE checkout.
- Seed histórico para relatórios e reconciliação: `SIMULACAO_DATABASE_NAME`, `seed_simulacao_historica.py`, `reconcile.py`, `ck_apontamentos_quantidade_atendida_planejada`, `gate=FAIL`
  - desc: Carga de três meses em banco dedicado, com health da API temporária aprovado mas reconciliação 187/204; cwd=Gestor de Peças TESTE checkout. Não tratar como homologação completa.
- TOTVS, homologação e factory bot: `GPOPSYNC`, `MATI650`, `WSPCP`, `ProductionOrder`, `idempotency_key`, `simular_fabrica.py`, `PcfIntegService`
  - desc: Contratos inbound/outbound, E2E controlado, reconciliação e fronteiras de outbound; cwd=Gestor de Peças TESTE checkout.
- Andon, Web TV, administração e design aprovado: `AndonResourceDrawer`, `WeldingManagementPage.tsx`, `Designs aprovados/Telas`, `FilterBar`, `analytics_filter`
  - desc: UI de TV/gestão, filtros, responsividade e constraints de assets; cwd=Gestor de Peças TESTE checkout.
- Refactor, Git e arquitetura legado: `3e93a6a`, `PySide6`, `QThread`, `Qlik Engine`, `mes/services`, `app/database`
  - desc: Refactors estruturais seguros, commits e contexto desktop legado; reexaminar checkout atual antes de aplicar.
- OEE/Corte, Telegram, relatórios e servidor TESTE (2026-09-21): `sem_demanda`, `telegram_cut.py`, `TelegramPresenter`, `telegram_corte_mensagens`, `SigmaNestSyncService`, `report_workbook`, `reiniciar_build.py`, `setup_exige_inicio`
  - desc: Correções operacionais, interface privada/routing Telegram e mensagens de Corte, planos SigmaNEST pré-MES, Excel/IagoDev e ciclo local; cwd=Gestor de Peças TESTE checkout. Para UI visual-only, consultar também `PPI`, `WEG`, `Eryxon Flow` e `Robô de Solda`.

#### Windows host maintenance

- Energia, perfis, Docker, display, webcam e biometria: `powercfg`, `Ultimate Performance`, `WinBioOpenSession`, `Win32_UserProfile`, `75 Hz`
  - desc: Manutenção específica deste host Windows; redescobrir estado e preservar dados.
- Compactação ZIP com validação: `CMD`, `Compress-Archive`, `zero-byte-archive`, `Length 0`, `7z`, `tar`, `Failed to open`
  - desc: Falha de ZIP vazio e `tar` abrindo destino no host Windows; para CMD, use fallback PowerShell com caminhos citados, mas exija tamanho não zero e lista/inspeção antes de entregar.

#### Other workflows

- Codex skills, contexto/export e projeto vazio: `Codex skills`, `$CODEX_HOME/skills`, `AGENTS.md`, `NO_FILES`
  - desc: Reconhecimento formal de skills, roteamento de memória e inicialização leve.
- AVA UNIASSELVI: `AVA UNIASSELVI`, `diagnostic-assessment`
  - desc: Contexto isolado de suporte educacional; não misturar com Gestor de Peças.
