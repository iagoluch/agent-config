---
name: pontos-alinhamento-lancamento-piloto-totvs
description: Pontos discutidos em reunião de alinhamento (14/09/2026) sobre o lançamento do piloto e a integração real com o TOTVS
metadata: 
  node_type: memory
  type: project
  originSessionId: f83a3722-14b5-48ff-b577-fec32a3b058e
  modified: 2026-09-14T19:54:14.796Z
---

Reunião de alinhamento em 14/09/2026 sobre o lançamento do piloto do Gestor de Peças, com foco na integração real com o TOTVS. Anotações do usuário (não literais, pontos da conversa).

**Why:** definem arquitetura e regras de negócio da integração de produção antes de sair do ambiente de testes, e ficaram pendências técnicas/de decisão em aberto.

**How to apply:** usar como referência ao planejar/implementar a integração TOTVS real; confirmar com o usuário qualquer ponto ainda em aberto antes de implementar.

Pontos levantados:

1. **Integração TOTVS real** — replicar a integração de teste; só divergir se algo realmente exigir diferença (anotação pessoal do usuário, ainda não validada com o time).
2. **Infra**: será lançada uma VM com Docker + banco de dados. URL terá acesso somente interno (requisições via API), sem precisar expor URL como parâmetro no TOTVS.
3. **Sincronização**: Gestor de Peças deve atualizar conforme o TOTVS recebe dados novos/atualizações de OP (quantidade alterada, data, etc — tudo).
4. **Observabilidade**: log literal em console para acompanhar tudo.
5. **Resiliência de conexão**: como lidar com quedas de conexão sem travar o sistema — pendência de definição técnica.
6. **Devolução de etapas ao TOTVS**: cada etapa apontada deve ser devolvida ao TOTVS; recursos que não existem no TOTVS (ex.: Destaque) devem ser ignorados no envio, mas atualizados/consolidados quando a OP chegar na próxima etapa que o TOTVS reconhece.
7. **Regra do TOTVS**: não aceita apontamento de OP com menos de 1 minuto de duração.
8. **Risco**: finalização parcial da OP pelo PCP pode conflitar com o Gestor de Peças tentando apontar uma OP que já foi fechada do lado do TOTVS — tratamento ainda não definido.
9. **Banco de dados**: empresa usa MSSQL por padrão; está em avaliação migrar ou manter Postgres no Gestor de Peças — decisão de negócio/infra em aberto.
10. **Futuro (fora do escopo do piloto agora)**: ao finalizar corte, fazer requisição ao SigmaNEST para dar baixa no banco.
11. **Fluxo Corte → Almoxarifado**: OP que sai do Corte passa por Inspeção antes de finalizar no Almoxarifado; já o fluxo que passa pelo Destaque não tem inspeção.
12. **Cadastro de filial**: começar a registrar a filial de origem da OP nos casos em que ainda não é registrada.

Pendências originais (todas decididas em 14/09/2026, ver seção abaixo). Único item que segue de fato futuro/fora do piloto:
- integração com SigmaNEST para baixa automática no banco ao finalizar corte (futura, não é pendência do piloto).

**RESOLVIDO (já implementado antes de 14/09/2026, confirmado nesta reunião)** — retry/reconexão TOTVS: outbox transacional com worker em background ([mes/integrations/totvs/outbox.py](../../mes/integrations/totvs/outbox.py), [TotvsOutboxWorker](../../mes/services/totvs_outbox_worker.py) ligado em backend/api/main.py), backoff 1/2/5/10/30/60min até 12 tentativas, 3 tentativas para erro de credencial, rejeição de negócio do TOTVS não é reenviada. Recebimento SOAP é stateless (quem reenvia em queda é o próprio TOTVS). Pull GPOPSYNC já homologado (ver etapa7b). Não é mais pendência real, só precisa confirmar se o worker está habilitado no ambiente do piloto.

**SUPERADO 21/09/2026: a infra fixou Windows Server 2025 + NSSM + nginx, sem Docker; ver docs/REQUISITOS_INFRAESTRUTURA_VM.md.** Histórico — 14/09/2026, distro Linux da VM Docker: recomendado e decidido **Ubuntu Server 24.04 LTS** (chefe pediu recomendação; sem padrão prévio na empresa). Motivo: suporte oficial Docker de primeira classe, LTS até 2029, sem custo de licença, maior comunidade/documentação. RHEL-family (Rocky/Alma) só faria sentido se já houvesse infra RHEL na empresa — não é o caso.

**DECIDIDO 14/09/2026 — OP fechada no TOTVS via finalização parcial do PCP** (pendência 2): tecnicamente já não quebra nada (rejeição `A680OPTOT Operacao ja totalizada` é classificada como FUNCTIONAL no outbox, não entra em retry infinito, ver [outbox.py:160](../../mes/integrations/totvs/outbox.py)). Faltava processo — decisão do usuário:
1. Notificar o supervisor via **Telegram** quando ocorrer a rejeição.
2. Ficar registrado como pendência para o supervisor decidir o que fazer (não há resolução automática).
3. Frequência esperada: ocasional, mas pode ficar frequente dependendo das pendências das máquinas — não é caso raro, vale a pena implementar já (não adiar).
Ainda não implementado — próximo passo natural é integrar bot/webhook do Telegram no ciclo do `TotvsOutboxWorker` quando um item cai em `ERROR`/`FUNCTIONAL`.

**DECIDIDO 14/09/2026 — MSSQL vs Postgres** (pendência 3): mantém **Postgres**, sem migração. Motivos: sistema já é acoplado nativamente ao Postgres (psycopg, advisory locks, migrations — ver [app/database/database.py](../../app/database/database.py)); a VM do piloto é isolada com banco próprio e acesso só via API interna, então não existe o problema de "padrão de banco compartilhado" que motivaria usar MSSQL; e MSSQL exige assinatura paga, sem benefício técnico que compense. Decisão fechada, não é mais pendência.

**DECIDIDO 14/09/2026 — cadastro de filial da OP** (pendência 4): piloto roda só na **filial 4**. Regra de negócio já é segura hoje — o `codigo_recurso` gravado por operação vem sempre do roteiro daquela OP específica, nunca inferido por produto (ver [resource_mapping.py:35](../../app/core/resource_mapping.py)), então recurso divergente entre matriz e filial 4 não é risco. Falta apenas implementar: quando o TOTVS não mandar `branch_id`, usar **"4" como valor padrão** em vez de gravar vazio (hoje grava string vazia, ver [database.py:439](../../app/database/database.py)). Ainda não implementado.

---

**STATUS GERAL 14/09/2026**: as 4 pendências reais do lançamento do piloto foram todas decididas nesta conversa. Falta apenas a IMPLEMENTAÇÃO combinada, a ser feita junto no final (conforme pedido do usuário — "lá no final quando a gente for implementar o que dá dos pontos que levantei"):
1. Notificação Telegram ao supervisor quando outbox cair em rejeição FUNCTIONAL (OP já totalizada).
2. (Postgres — nenhuma ação necessária, decisão de manter como está.)
3. Default de filial="4" quando `branch_id` vier vazio do TOTVS.
