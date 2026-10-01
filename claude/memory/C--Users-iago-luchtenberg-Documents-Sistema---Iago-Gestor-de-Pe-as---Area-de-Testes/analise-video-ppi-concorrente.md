---
name: analise-video-ppi-concorrente
description: "Análise de 21/09/2026 do vídeo 'A Rotina de um Operador no Sistema MES' (WEG PPI-Multitask/PC-Factory, concorrente direto) — pontos fortes a adaptar, onde o Gestor de Peças já é melhor, e o que a PPI faz mal."
metadata: 
  node_type: memory
  type: project
  modified: 2026-09-21T18:21:58.433Z
  originSessionId: 75e7da9f-f422-46b4-9db7-52a8b071fa8b
---

Vídeo analisado: https://www.youtube.com/watch?v=KYS1JlIBIdc (canal "WEG PPI-Multitask Oficial", ~4:50, sem transcript disponível — assistido via screenshots manuais). PPI é o concorrente que o usuário está desbancando com o Gestor de Peças.

**Why:** usuário pediu para guardar como ponto de backlog, NÃO implementar sem OK explícito ("Guarde esse ponto para fazer depois do meu ok").

## Pontos fortes deles, candidatos a adaptar (com ajustes, não copiar)

**REJEITADOS 21/09/2026** — ver [[feedback-simplicidade-chao-de-fabrica]]: usuário tem experiência de chão de fábrica e afirma que operadores reais não seguem esse tipo de passo extra; só reconsiderar se um superior pedir explicitamente.

1. ~~Bloqueio de recurso por qualificação do operador com autorização de supervisor~~ — rejeitado.
2. ~~Leitura obrigatória de documento técnico/desenho antes de iniciar produção~~ — rejeitado.
3. ~~Checklist de setup com foto de referência + Aprovado/Reprovado~~ — rejeitado.
4. ~~Apontamento dedicado de troca de ferramenta~~ — rejeitado.
5. **Dashboard de piso de fábrica** com indicador verde/vermelho por setor, visão de gestor em nível de planta — CONTINUA VIVO. Usuário já tem a planta baixa real da fábrica (mapa de manufatura) e quer usar como base visual do dashboard.

## Onde o Gestor de Peças já é mais refinado

- Gate **Setup→Qualidade→popup→retomada automática** (Wave 6A/6B) é mais integrado que a tela de setup deles (parece isolada, sem retomada automática visível).
- **Andon com rodízio** e distinção **recursos apontáveis vs. só sincronizados** não aparecem no material deles — tratam todo recurso igual.
- Modelagem da **Solda em 5 setores** (Aço/Alumínio/Robô/Ferramentaria/Protótipo) é mais granular que qualquer segmentação mostrada.
- Retry/backoff no outbox TOTVS (`mes/integrations/totvs/outbox.py`) parece mais resiliente — na demo deles não há tratamento visível de falha de sincronização com ERP.

## O que a PPI faz mal

- Tela final **"Eventos de Produção"** é uma grade densa/genérica (Table/WorkStep/Simplificado) sem visualização amigável — inconsistente com o polimento do dashboard de piso mostrado antes na mesma demo.
- "Reorganização automática da view de produção" parece efeito colateral de layout responsivo, não feature intencional — não demonstra resolver um problema real do operador.
- Nenhum tratamento de erro de sincronização ERP demonstrado — ponto cego que já cobrimos.

## Próximo passo (não decidido, só anotado)

Se o usuário aprovar, a ordem natural seria: (1) gate de qualificação operador×recurso com autorização supervisora, (2) leitura obrigatória de documento antes de produzir, (3) checklist de setup com foto, (4) apontamento dedicado de troca de ferramenta. Nenhum implementado ainda.

Ver também [[inspiracao-mes-eryxon-e-concorrentes-br]] (mesma lógica: inspiração sem cópia literal, aguardando OK).
