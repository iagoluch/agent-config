# Gestor de Peças - Area de Testes

## Objetivo
Sistema de MES (Manufacturing Execution System) para a fábrica ("Sistema - Iago"),
cobrindo apontamento de produção, calendário/OEE, Andon, integração com TOTVS
Protheus e SigmaNEST, e um bot de Telegram para chamadas/planos de corte.

## Stack (FATO)
- Backend Python (módulo `mes/`, `backend/api/`).
- Frontend React/TypeScript (`web/src/pages/...`).
- Testes em `tests/` (pytest, presumivelmente).
- Scripts Node/JS de verificação em `tools/*.mjs`.
- Git como controle de versão; branch principal `master` (branch de trabalho
  também chamada `main` em outras convenções — confirmar antes de abrir PR).

## Decisões importantes
- Ver histórico completo em `~/.claude/brain/decisions/` e nas memórias de
  wave (arquivos `wave*-estado.md` no diretório de memória do projeto) — não
  duplicar aqui; apontar para lá.
- Integração com Protheus/AdvPL vive em repositório separado (regras
  CP-1252/RDMake/AdvPL nunca entram neste repo Python).

## Estado atual (FATO, 22/09/2026)
- Os commits `f838f66`, `282b305` e `bf34f2f` foram publicados em `master`:
  atividade sem OP como estado físico canônico (schema 42), ajustes do posto
  Corte/Destaque e navegação/indicadores, e consulta privada de recursos por
  frente no Telegram. A classificação de falhas HTTP TOTVS foi centralizada.
- O worktree mantém somente WIP não commitado: `scripts/resetar_banco_teste.py`,
  `scripts/clean-junk.ps1` e `scripts/register-clean-junk-task.ps1`.
- A consulta de estado atual agora leva a taxonomia do catálogo: `0009 — PAUSA
  PARA CAFÉ` é parada programada pelo grupo `0002`, inclusive se o operador a
  lança manualmente. O Andon une `LASER1` e `Laser Ensis 3015` pela identidade
  canônica e não apresenta fila sem OP como estado operacional.
- No banco `gestor_pecas_test`, as OPs `PCMITL01001` e `PCMIDN01017` foram
  resetadas apenas na execução de Dobra; o planejamento inbound e os 16
  apontamentos de Corte finalizados foram preservados. A próxima etapa das duas
  é Dobra.
- Setup requer o Início prévio da mesma OP. A regra está no domínio/API
  (`setup_exige_inicio`) e o botão do posto só habilita com apontamento ativo.
- Os hooks locais do Codex foram alinhados aos recentes hooks próprios do
  Claude: Graphify e type-check TS foram preservados; Ponytail, Headroom e
  seu autostart foram incluídos. O OmniRoute não inicia mais automaticamente
  no Codex; continua opcional. Os hooks usam o Git Bash com caminho explícito.
- A skill Impeccable v4.3.1 está vinculada ao catálogo global do Codex e seu
  detector visual foi habilitado no projeto: `PostToolUse` após edição e
  revisão profunda no evento `Stop`, sem remover os hooks já ativos.
- A auditoria de paridade Claude→Codex foi consolidada em
  `docs/CODEX_PARIDADE_CLAUDE.md`. O Task Observer foi vinculado como skill
  global do Codex e recebeu um hook SessionStart; a confiança nativa desse
  hook ainda precisa ser aprovada em uma nova sessão. O inventário completo
  revelou 900 skills do Claude: as 832 automações Composio foram espelhadas
  arquivo a arquivo em `~/.codex/skill-library/composio-skills` e são
  carregadas pela skill de catálogo sob demanda; as 68 restantes permanecem
  nativas/compartilhadas. O limite de instruções foi ajustado para 96 KB e
  carrega integralmente o `AGENTS.md` de 72,5 KB.
- O MCP Headroom foi restaurado sem rede da cópia cacheada `headroom-ai 0.37.0`
  com o extra oficial MCP. O registro Codex aponta diretamente para o ambiente
  `uv`; `initialize` e `headroom_compress` foram validados por stdio. A política
  global de aprovação `never` ainda impede que um agente invoque a ferramenta
  MCP que pede aprovação, mas não impede o servidor de iniciar.
- O MCP `pg_aiguide` respondeu a `initialize`, `tools/list` e `search_docs`
  somente-leitura. O OmniRoute continua registrado, porém sem operação de
  ferramenta comprovada.
- FATO (23/09/2026): o Andon não descarta mais recurso ativo de Montagem nem
  de setor ainda não classificado. O backend publica `Montagem` ou `Não
  classificado` sem inferir equivalência; a UI respeita os painéis e sua ordem
  no contrato. Commit publicado: `05ebe2a`.
- FATO (23/09/2026): a outbox TOTVS passou a ordenar a entrega por OP. Todo
  item anterior não enviado (`PENDING`, `RETRY`, `SENDING` ou `ERROR`) bloqueia
  o posterior, e a migration 46 normaliza os itens já gravados para a chave da
  OP antes de criar o índice de suporte. Commit publicado: `4ecac64`.
- FATO (23/09/2026): a exclusividade agora cobre toda transição para estado
  ocupante, inclusive `Aguardando` para `Parada`; o lock e a comparação usam a
  identidade canônica de recurso. Commit publicado: `3ec7ddf`.
- FATO (23/09/2026): exceções de recurso divergente e etapa anterior pendente
  exigem o mesmo crachá responsável já usado no fluxo de refugo/retrabalho;
  crachá somente ativo não libera exceção. Commit publicado: `7dfbf07`.
- FATO (23/09/2026): sessões principais carregam `session_version`; alteração
  de senha, nível ou ativação incrementa a versão no PostgreSQL e invalida
  tokens anteriores. Migration 47 e commit publicado: `f52c37c`.
- FATO (23/09/2026): o freio de autenticação principal e do Dev Observatory
  persiste contadores por usuário + IP na tabela `login_throttle`, com janela
  de expiração e chave Cloudflare validada apenas no caminho público confiável.
  Migration 48 e commit publicado: `779427f`.
- FATO (23/09/2026): `parametros_turno` agora é propagado pela mesma instância
  de regras para calendário global, auditoria de limites e capabilities Web;
  fallback deixou de reconstruir a janela fixa. Commit publicado: `fe1b87e`.
- FATO (23/09/2026): o calendário produtivo por recurso ganhou escritores
  administrativos com CSRF para calendário, turnos e vínculo de recurso;
  migration/schema não foram duplicados. Commit publicado: `34fc44b`.
- FATO (23/09/2026): o POST de relatórios do Dev Observatory exige CSRF
  próprio da sessão assinada da ferramenta; o cookie e o header são
  comparados, e o logout remove ambos. Commit publicado: `76117cb`.
- FATO (23/09/2026): apontamentos operacionais guardam o ID imutável do
  crachá principal no Início/Fim. Participações são únicas por ID e resolvem
  nome/crachá na leitura; texto antigo permanece só como fallback legado, sem
  associação inferida. Commit publicado: `b3b0fb8`.
- FATO (23/09/2026): o inbound SOAP TOTVS agora verifica o IP/CIDR observado
  no socket antes de ler WSDL ou mensagem. Sem allowlist a aplicação inicia,
  mas o receptor retorna 503; Host e X-Forwarded-For não autorizam origem.
  O Dev Observatory também recusa credencial com qualquer privilégio efetivo
  de escrita/DDL, apesar da sessão read-only. Commit publicado: `8f0aa6c`.
- FATO (23/09/2026): existe backup local verificável do TESTE pelo
  `scripts/backup_banco_teste.py`: exige confirmação literal, produz dump
  custom, valida com `pg_restore --list` e grava SHA-256. Um dump do
  `gestor_pecas_test` foi criado/validado; retenção, cópia externa e ensaio de
  restauração continuam decisão operacional. Commit publicado: `76c2cac`.

## Bloqueios conhecidos
- Não commitar o reset com preservação de OPs: a contagem esperada subtrai as
  OPs preservadas duas vezes e não há cobertura para a nova opção.
- Não ativar a limpeza agendada: ela remove `_quarentena_revisar/` contra a
  regra atual e usa nome de tarefa diferente do registrado anteriormente.

## Próximo passo
- Determinar pelo pedido atual do usuário; não presumir.
