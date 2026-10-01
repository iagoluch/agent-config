---
name: solda-5-setores-especificacao
description: "Especificação fechada (14/09/2026) de como o antigo setor único 'Solda' vira 5 setores reais: Solda Aço, Solda Alumínio, Solda Robô, Proj. Ferramentaria, Protótipo. Contas/logins, recursos TOTVS por setor e regras confirmadas."
metadata: 
  node_type: memory
  type: project
  originSessionId: cf9cf250-080d-46c0-be6f-81d695cbf05f
  modified: 2026-09-14T19:37:09.069Z
---

Em 14/09/2026 o usuário fechou a especificação de como a Solda vai se dividir. Isso substitui/complementa [[regra-recursos-apontaveis-vs-sincronizados]] (que tinha o plano ainda em aberto).

## Os 5 setores, contas e recursos TOTVS

| Setor | Contas/login | Recursos do catálogo (código bruto TOTVS) |
| --- | --- | --- |
| **Solda Aço** | `estacao1aco`..`estacao10aco` (10) | os 41 códigos legados que sobraram de "Solda" (tudo exceto ROBO P/S e SOLDA4) |
| **Solda Alumínio** | `estacao1alu`..`estacao6alu` (6) | nenhum ainda — setor nasce vazio, igual Montagem hoje |
| **Solda Robô** | `robo1` (1) | `ROBO P` (49 usos reais em roteiro), `ROBO S` (170 usos reais) |
| **Proj. Ferramentaria** | `projetos` (1) | `DISPEX` (Dispositivos Exportação), `DISPG` (Dispositivos Genéricos), `SERVGE` (Serviços Gerais), `DISPOS` (Reforma de Dispositivos) |
| **Protótipo** | `prototipo` (1) | `PREMTG` (Pré-Montagem), `SOLDA4` (Soldagem) |

**Números de estação/conta são variáveis** — a Manufatura ainda vai confirmar quantos quiosques físicos cada setor realmente usa. Os números acima (10/6/1/1/1) são o ponto de partida, não definitivo.

## Regras confirmadas (perguntei, usuário respondeu explicitamente)

1. **São 5 setores reais e distintos**, não só nomes de conta — cada um tem seu próprio `tipo_setor`, elegibilidade e aparência no sistema (não é tudo "Solda" por baixo).
2. **Todos seguem a regra aberta** (mesma lógica de Solda Aço = pertencimento por `tipo_setor`, "qualquer recurso do setor é apontável") — inclusive Proj. Ferramentaria e Protótipo, que têm só 2-4 recursos nomeados hoje mas não ficam travados numa lista fechada.
3. **Sem bloqueio de recurso divergente** em nenhum dos 5 (mesma exceção que já vale pra "solda" desde o commit `44675f3` — usuário confirmou "mesma lógica da solda aço" para Alumínio/Robô, e a resposta sobre elegibilidade aberta reforça que vale para os 5).
4. **Andon**: os 5 aparecem como **sub-grupos dentro de 1 painel "Solda"** — mesmo padrão que o Corte já usa hoje pra Laser/Plasma/Destaque. Não viram 5 painéis de topo separados.
5. **Os 41 recursos legados de Solda Aço ficam no banco (tipo_setor='Solda Aço'), mas NÃO podem aparecer em nenhuma tela/listagem por padrão** — só "vêm para frente" reativamente se uma OP real algum dia referenciar um deles no roteiro (`catalogo_operacoes_op`). Isso é regra específica desses 41 códigos, não uma regra geral de ocultar tudo sem uso.
6. **Senha das contas novas**: `1234`, só em TEST. No lançamento em produção, o usuário vai trocar manualmente — pediu um "card no Dev Observatory" como lembrete; se esse mecanismo de card/pendência não existir hoje no Dev Observatory, não inventar do zero, só registrar a pendência de forma simples e avisar o usuário.

## Ajuste de UX confirmado (commit `f37c3f8`)
Dentro da frente de Solda, nem todo setor tem posto fixo por login: **só Solda Robô** fica fixo (login `robo1` vai direto ao apontamento). **Proj. Ferramentaria** e **Protótipo** são conta única cobrindo vários recursos nomeados do cadastro (DISPEX/DISPG/SERVGE/DISPOS e PREMTG/SOLDA4) — o login pede seleção de recurso na tela, igual Dobra/Usinagem/Serra, antes de ir para o mesmo formulário de apontamento. Solda Aço/Alumínio continuam 1 login = 1 posto fixo (era o comportamento correto desde o início). Causa raiz de um bug relatado antes deste ajuste: um processo de API antigo/desatualizado (porta 8001, o mesmo "fantasma" que resiste a `taskkill` a sessão inteira) ainda rodava o código de ANTES da Wave 6F, então `estacao1aco` não era reconhecido e caía no nível padrão `operador_destaque` → ia pra tela de Destaque. Não era bug de código — confirmar sempre contra um processo com o código atual antes de investigar mais fundo.

## Status: IMPLEMENTADO e confirmado pelo usuário em 14/09/2026
As 5 decisões do agente foram todas aprovadas sem ajuste. Pausas automáticas (só Solda Aço tem horário configurado) foi confirmado como intencional — usuário disse explicitamente "deixa como está" para os outros 4 setores, não é pendência. `RESOURCE_FRIENDLY_NAMES["SOLDA4"]` corrigido de "Solda" para "Soldagem" (commit `d996e10`), confirmando que SOLDA4 pertence ao Protótipo.

## Onde isso foi implementado
Delegado a um agente `hard` em 14/09/2026 (mesma sessão). Arquivos-alvo: `app/core/operator_sectors.py` (contas novas), `app/core/resource_mapping.py` (`SECTOR_OWNED_RESOURCE_SECTORS`, `RESOURCE_CONFIRMATION_EXEMPT_SECTORS`), `mes/services/andon.py` (agrupamento visual), `catalogo_recursos_pcfactory` no `gestor_pecas_test` (reclassificação de `tipo_setor`), e a tela de Capacidade (`listar_configuracao_capacidade_recursos`, já era bug conhecido — ver [[regra-recursos-apontaveis-vs-sincronizados]]) para respeitar a ocultação dos 41 legados. **Conferir o resultado real antes de assumir que ficou pronto** — esta memória registra a especificação, não necessariamente o estado final do código.

Ver também [[regra-recursos-apontaveis-vs-sincronizados]] para o histórico da investigação que levou a esta especificação (os 2 bugs achados, a lista completa dos 44 recursos originais, etc.).
