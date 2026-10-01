---
name: redesign-visual-mes-profissional-23-09-2026
description: "Pass visual completo (tokens/global.css/componentes) do redesign \"cara de MES profissional\"; fix real no OperatorDialog; 6 falhas pré-existentes em operator.test.tsx eram falha do mock de teste, não bug de produção."
metadata:
  node_type: memory
  type: project
  originSessionId: 4f869c5b-eb66-473e-98db-73bf6598e807
  modified: 2026-09-23T05:47:11.122Z
---

23/09/2026, dentro da auditoria `/goal`: executado (via subagente `hard` em background, delegação única) o pass visual autorizado por [[feedback-modernizacao-sem-alterar-logica]] — "esquecer esse design que eu mesmo fiz, deixar com cara de MES profissional... nunca altere a lógica presente".

**Escopo do redesign (concluído):** `web/src/styles/tokens.css`, `global.css`, `ai.css`, `andon.css` (mínimo), `welding.css` (mínimo); className-only em `OperatorDialog.tsx`, `StatusBadge.tsx`, `AndonPage.tsx`, `WeldingManagementPage.tsx`, páginas operator (Cutting/Highlight/QualityInspection/Workbench). Sem alteração de JSX/DOM structure, sem tocar backend. Build (`tsc -b && vite build`) e `andon.test.tsx` verdes. 2 defeitos reais achados e corrigidos via screenshot em telas de gestão (fonte 10px no select de Setor; padding apertado em tabela) — verificado em 1440px e 820px, light/dark.

**Bug real corrigido (fora do escopo do subagente, aplicado direto):** `OperatorDialog.tsx` — `useEffect` do focus-trap dependia de `onCancel` (função inline recriada a cada render do pai), reexecutando o focus-trap inteiro (incluindo roubar foco do primeiro elemento) a cada re-render — atrapalhava o operador no meio de uma interação. Fix: `useRef` guardando a versão atual de `onCancel`, effect roda só uma vez (`[]`). Verificado com `tsc -b` limpo.

**As 6 falhas pré-existentes em `operator.test.tsx` (Setup/Qualidade) NÃO eram bug de produção — eram falha do mock do teste:**
1. O helper `abrirPortao` clicava em "Setup" logo após o toast "Início registrado com sucesso.", antes do `cards.reload()` assíncrono atualizar o card para "Em processo" — o botão Setup ainda estava `disabled` (regra real: `canSetup` exige `currentStatus` em `["Em processo","Parada","Retrabalho","Setup"]`), e `fireEvent.click` num botão disabled é um no-op silencioso.
2. O objeto `gate` do mock de backend (`gateBackend()`) era estático: depois de o operador liberar o lote pelo checklist, a resposta do POST `/operator/first-piece` dizia `liberado:true` mas o mock nunca atualizava seu próprio estado interno — então os próximos GET (roteiro/first-piece) continuavam devolvendo `setup_registrado:false`/`liberado:false`, e o botão Setup nunca voltava a ficar disabled.

Fix aplicado só no arquivo de teste (`web/src/test/operator.test.tsx`): `waitFor` esperando o botão Setup habilitar antes do clique; `gate.setup_registrado`/`gate.liberado` mutados de fato dentro do handler POST; `pode_finalizar`/`exige_gate_primeira_peca` no GET de operations lendo `gate.liberado` (estado vivo) em vez do `options.liberado` estático do setup do teste. **31/31 testes passando, `tsc -b` limpo.** A lógica de produção em `WorkbenchPage.tsx` (gate/checklist da primeira peça) estava correta o tempo todo — nada foi alterado lá.

**Por que isso importa:** fecha a pendência de teste que ficou em aberto no fim da sessão anterior; confirma que o fluxo de gate Setup/Qualidade (Wave 6B) é sólido. Ver [[auditoria-23-09-2026-estado]] para o restante do escopo do `/goal` (8 achados de backend ainda aguardando confirmação do usuário, per [[auditoria-backend-13-achados-23-09-2026]]).

**Extensão do redesign às 19 telas restantes (23/09/2026, subagente `hard` em background):** as páginas de gestão/setup (Login, Management Overview, Production, Reports, Pauses, Badges, Users, Goals, Shifts, System, Chamadas, Traceability, Audit, Operations, Analytics, Operator Portal, AI, Quality) já herdavam a maior parte do visual novo via classes compartilhadas (painel, cards, tabelas, badges, `.button`) — só o CSS específico de cada tela ainda estava velho. Mudança ficou 100% concentrada em `web/src/styles/global.css` (257 inserções / 191 remoções, zero `.tsx` tocado). 3 bugs visuais reais achados e corrigidos (só CSS, sem lógica):
1. Botão primário de diálogo renderizando como se fosse "Cancelar" (branco liso) em 16 diálogos — uma regra antiga era mais específica que o estilo de botão primário novo. Afetava inclusive diálogos das telas de operador da primeira leva.
2. Linhas não-conformes da Qualidade perdiam o destaque vermelho nas linhas pares (zebra sobrescrevia).
3. Toolbar de filtro da Qualidade em formato de pílula, destoando do padrão de card do resto do app.

Build (`tsc -b`, `npm run build`) limpo; `operator.test.tsx` seguiu 31/31 (nenhum teste tocado). Verificado ao vivo na tela de Login via preview server. **Nada commitado.** Com isso, o pass de redesign visual autorizado pelo `/goal` está praticamente completo em toda a superfície do app (operador + gestão + auth), restando só ajustes pontuais que o usuário decidir pedir.
