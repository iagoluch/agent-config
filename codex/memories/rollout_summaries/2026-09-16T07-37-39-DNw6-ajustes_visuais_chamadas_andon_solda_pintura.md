thread_id: 01a0a926-600e-7c40-adef-5c8575b41ba2
updated_at: 2026-09-15T17:49:15+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\16\rollout-2026-09-16T04-37-39-01a0a926-600e-7c40-adef-5c8575b41ba2.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Ajustes de interface, chamadas e fluxo operacional concluídos

Rollout context: Trabalho no repositório `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`, envolvendo a tela inicial da gestão, telas de operador, chamadas, Andon e tema visual.

## Task 1: Ajustes visuais e de interação

Outcome: success

Preference signals:
- O usuário pediu que as tarefas de Corte ficassem com o dropdown fechado por padrão.
- O usuário pediu botões apontáveis centralizados e redimensionados para todos os setores, não apenas Corte.
- O usuário esclareceu que os cards “bagunçados” eram da tela inicial da gestão/Visão Geral, e não de uma página chamada Dev Observatory. Futuras descrições devem usar “tela inicial da gestão” ou `ManagementOverviewPage`.

Key steps:
- Tarefas de Corte passaram a iniciar recolhidas.
- O grid manual dos botões do operador foi substituído por layout flexível centralizado em `global.css`/`WorkbenchPage.tsx`.
- Listas curtas dos cards da Visão Geral passaram a centralizar verticalmente.
- Corrigido o tema escuro: faltava `color-scheme`, fazendo campos exibirem texto claro sobre fundo branco nativo; backgrounds explícitos foram adicionados aos campos afetados.
- Cores fixas da tela de IA foram substituídas por tokens do tema e foi adicionado piso mínimo para a área de mensagens em janelas baixas.

Validation: build Vite/TypeScript passou; testes frontend afetados passaram.

## Task 2: Chamadas configuráveis por setor

Outcome: success

Key steps:
- Contatos de chamada passaram a ter `setores TEXT[]`, configurável na tela de Chamadas.
- O dropdown do botão de chamada filtra contatos pelo setor do operador.
- A migration foi adicionada, mas inicialmente `SCHEMA_VERSION` permaneceu em 35; isso impediu a aplicação da migration 36 e quebrou o cadastro.
- Corrigido para schema 36, backend reiniciado e coluna confirmada no banco.
- O script de limpeza do banco de teste foi atualizado para classificar `chamadas` e `chamada_visualizacoes` como dados operacionais, mantendo `chamada_contatos` protegido.
- O banco `gestor_pecas_test` foi limpo com preservação de schema e cadastros; o banco real foi verificado somente leitura.

Validation: 31 testes de chamadas passaram; migration aplicada; schema 36 confirmado. Commits relevantes: `019d163` e `c176db7`.

Failures and how to do differently:
- Ao adicionar migrations, sempre atualizar `app/database/schema.py:SCHEMA_VERSION` e reiniciar processos sem `--reload`.
- Atualizar fakes de teste quando endpoints ganharem novos parâmetros.

## Task 3: Andon e finalização na Solda/Pintura

Outcome: success

Key steps:
- Corrigido bug em que uma OP em execução era publicada no Andon como “Sem demanda”: `ops_ativas` era zerado antes da decisão de domínio e o retorno de turno vencia a evidência de execução.
- Execução ativa agora sempre vence `explicit_shift_return`; Corte com nesting ativo não é marcado como sem demanda.
- O marco terminal `99 - FINALIZADA` deixou de ser selecionável ou virar etapa atual; ele fica `done` após a última etapa real.
- Inicialmente foi criada uma conferência de primeira peça para Solda/Pintura, mas o usuário esclareceu: “solda e pintura tem esquema de qualidade diferente... fica como mais um recurso apontável só pra contar tempo”.
- A política final exclui Pintura e todos os setores da família Solda do portão de primeira peça; Finalizar funciona diretamente como recurso de apontamento de tempo.

Validation: 394 testes backend afetados passaram; 29 testes frontend do operador passaram; `tsc --noEmit` limpo; build concluído; backend reiniciado na porta 8001. Commits relevantes: `fbde537` e `f8dc1c8`.

Reusable knowledge:
- A política de primeira peça é centralizada em `mes/domain/first_piece.py`, através de `first_piece_applies()`. Alterar `SECTORS_OUTSIDE_FIRST_PIECE` propaga a decisão para criação do registro, `pode_finalizar` e validações dependentes.
- Solda e Pintura não devem receber Setup, checklist ou conferência de primeira peça no Gestor; seus postos servem para Iniciar/Parada/Finalizar/Retrabalho e contagem de tempo.

References:
- `web/src/pages/ManagementOverviewPage.tsx`: tela inicial da gestão/Visão Geral.
- `mes/domain/first_piece.py`: `SECTORS_OUTSIDE_FIRST_PIECE`.
- `app/database/schema.py`: `SCHEMA_VERSION = 36`.
- `http://127.0.0.1:8001/api/v1/system/health`: backend validado com `schema_version: 36`.
