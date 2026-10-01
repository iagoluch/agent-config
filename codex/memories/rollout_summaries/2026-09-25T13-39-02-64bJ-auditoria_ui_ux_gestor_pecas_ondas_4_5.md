thread_id: 01a0d8ca-74f0-78c0-808d-99d7664077f7
updated_at: 2026-09-25T13:36:07+00:00
rollout_path: C:\Users\iago.luchtenberg\.codex\sessions\2026\09\25\rollout-2026-09-25T10-39-02-01a0d8ca-74f0-78c0-808d-99d7664077f7.jsonl
cwd: \\?\C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes

# Auditoria e correção incremental de UI/UX do Gestor de Peças

Rollout context: Projeto React/Vite com backend FastAPI em `C:\Users\iago.luchtenberg\Documents\Sistema - Iago\Gestor de Peças - Area de Testes`. O usuário exigiu auditoria rigorosa, correções por ondas, sem tocar na OEE, sem subagentes e com validação por testes, build e navegador.

## Task 1: Onda 4 — polish de UI, acessibilidade e Dev Observatory

Outcome: success

Preference signals:
- O usuário pediu análise individual e controle de uso: “Fique atento ao meu uso de 5 horas... se possível, analise sozinho” -> evitar subagentes e limitar chamadas.
- O usuário determinou que Andon/Solda serão exibidos em TV e pediu “não coloque botão em tv” -> não adicionar controles flutuantes nessas telas.
- O usuário quer mudanças rastreáveis por ID, com correção em componentes/tokens compartilhados e sem alterar OEE/lógica MES.

Key steps:
- Corrigidos itens OP-16/17/18/19, GE-12, IA-02, AX-07 e melhorias do Dev Observatory.
- Build validado e testes direcionados passaram: 86/86 e depois 41/41; `tsc` limpo.
- Dev Observatory validado com mensagens pt-BR, foco na senha após 401 e CSP preservada.
- Botão de tela cheia chegou a ser criado para Andon/Solda, mas foi removido após a preferência explícita do usuário; nenhum botão de TV permaneceu.
- Commit e push concluídos: `9260cdc feat(ui): onda 4 da auditoria — P3/polish de operador, gestão, IA e Dev Observatory`.

Failures and how to do differently:
- O teste visual do Andon confundiu rotação `/andon` → `/welding-management` com desaparecimento do botão. Em telas de TV, considerar sempre a rotação automática antes de classificar regressão.
- O fixture visual não implementa `contar_chamadas_nao_vistas`, causando 500 recorrente; registrar como limitação do harness, não como bug do produto.

Reusable knowledge:
- Playwright está disponível em `C:/Python314/python.exe`, não necessariamente no venv.
- Os previews 8010/8011 servem `web/dist`; executar `npm run build </dev/null` antes da inspeção visual.
- Firefox/WebKit não foram testados por falta de autorização para download.

References:
- `docs/auditoria_ui_2026-09-24/CORRECOES.md`
- Commit `9260cdc`
- `web/src/components/FilterBar.tsx`, `PageFrame.tsx`, `StopReasonFields.tsx`, `OperatorShell.tsx`, `global.css`
- `backend/api/routers/dev_observatory.py`

## Task 2: Onda 5 — regressão visual e matriz responsiva

Outcome: partial

Preference signals:
- O usuário pediu conclusão até 100%, mas a sessão terminou por limite antes do fechamento da Onda 5 -> futuras execuções devem priorizar concluir comparação, documentação e commit antes de novas melhorias.

Key steps:
- Criada matriz com 430 pares antes/depois cobrindo gestão, operadores e 10 tamanhos, incluindo reflow 320px.
- Resultado agregado: `hOverflow 110→80`, textos pequenos `11057→10403`, clipped `194→82`, alvos pequenos `579→120`, erros `1270→860`; não surgiram controles sem nome, inputs sem label ou imagens sem alt.
- Detector Impeccable permaneceu estável: 12 warnings pré-existentes, 0 novos.
- Web Vitals melhoraram em algumas rotas: OEE LCP 404→392ms, relatórios 340→316ms, operador INP 112→48ms, Andon 560→116ms.
- A maior parte das “pioras” era explicável por mudanças intencionais, como ordenação adicionada à tabela e títulos ocultos acessíveis.
- IA-01 parcialmente corrigido: títulos passaram a seguir “Seção — Aba”; permanece pendente decidir se “IagoDev” deve virar “Administração”.
- Ajustado o ícone de ordenação de tabela, identificado como texto de 9px.

Failures and how to do differently:
- A execução da matriz gerou muitos logs e exceções do fake database; usar sempre resumos e filtrar por endpoint.
- O comparador inicialmente tratou `h1.visually-hidden` como texto cortado; excluir explicitamente elementos visualmente ocultos ao interpretar métricas.
- O fluxo de regressão ainda não foi fechado com documentação/commit após os últimos ajustes.

Reusable knowledge:
- Script principal: `scratchpad/matrix.py`; saída pós-correção em `scratchpad/matrix_depois/`.
- Runner temporário: `scratchpad/regress.py`, que inicia o app visual em thread na porta 8013.
- Fluxos: `scratchpad/onda5_flows.py`; vitals: `scratchpad/vitals_depois.py`; comparação: `scratchpad/cmp_matrix.py` e `cmp_flows.py`.
- OEE deve continuar fora de qualquer alteração ou interpretação corretiva.

References:
- `scratchpad/matrix_depois/mgmt.json`, `dobra.json`, `corte.json`, `destaque.json`, `solda.json`
- `scratchpad/flows_depois/vitals.json`
- `scratchpad/detect_depois.json`
- `docs/auditoria_ui_2026-09-24/CORRECOES.md`

# Status final
A Onda 4 foi concluída e publicada. A Onda 5 tem evidências substanciais e resultados de regressão, mas ficou parcial porque a sessão atingiu o limite antes de anexar a seção final ao documento, executar o commit da Onda 5 e produzir o relatório final consolidado.
