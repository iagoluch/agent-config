# IAgo Company OS

## Objetivo

- FATO — Company OS local-first; S01 Digital Worker / AI BPO é o piloto.

## Stack

- FATO — Python, PostgreSQL e execução Task → Run → Step.
- FATO — Model providers implementam o contrato `core/model_provider.py`.

## Arquitetura

- DECISÃO — Modular monolith; PostgreSQL é a fonte de verdade e fila inicial.
- DECISÃO — Modelo/tier são resolvidos pelas configurações canônicas em `company/`.

## Decisões importantes

- DECISÃO — Codex CLI e Anthropic Messages API são providers equivalentes selecionáveis no mesmo AgentRuntime.
- DECISÃO — Anthropic usa `ANTHROPIC_API_KEY`, HTTP da biblioteca padrão e structured output por JSON Schema; segredos não entram em prompt, log ou Git.

## Estado atual

- FATO — Fases 0–10 e a implementação técnica 0–100% da Fase 11 estão concluídas na `main`; HEAD local do checkpoint operacional: `2dfe70a4147f173f37a7e6c0bc485dac722b12d0`.
- FATO — Gates do checkpoint: 160 testes Core, 28 Dashboard, 69 evals, 3 frontend unitários e 12 E2E aprovados; typecheck, build, compileall, pip check e contratos do repositório verdes.
- FATO — Provider Anthropic autentica por `x-api-key`; evidências de readiness têm sanitização recursiva; decisões de portfólio exigem CEO também na camada de domínio.
- FATO — Codex local autenticado passou smoke real; Claude Code está instalado, porém não autenticado neste ambiente.
- FATO — Ambiente local do notebook configurado sem `.ps1`: frontend Vite em `127.0.0.1:5173`, backend FastAPI em `127.0.0.1:8000` e PostgreSQL Docker `iago-company-os-phase3-pg` na porta `55434` com a base separada `iago_company_os` e migrations `0001`–`0014`.
- FATO — `IAGO_DATABASE_URL` e um `IAGO_CEO_TOKEN` aleatório estão persistidos no ambiente do usuário; o token não foi registrado em arquivo, Git ou memória.
- FATO — RevenueRun real `bff9087a-9d6f-4ef9-ac5f-6c9a0ce51b13` está `READY_FOR_OUTREACH`, com Opportunity `CONVERTED`, Initiative `RUNNING` budget US$ 0, Offer `READY` BRL 2.900 e três Leads reais `QUALIFIED`.
- FATO — Nenhum contato real, Deal, Customer, external effect, RevenueEvent ou pagamento foi registrado; a primeira receita continua não comprovada.
- FATO — O documento factual e o texto pronto de contato estão em `docs/FIRST_REAL_REVENUE_VALIDATION.md`.

## Bloqueios

- PENDENTE — A próxima operação é externa: Iago precisa enviar manualmente o e-mail preparado à SignaCon. Nenhum provider está autorizado ou activation-ready no banco operacional atual.
- PENDENTE — Claude Code ainda requer login interativo; Codex está operacional e foi o runtime efetivo do RevenueRun.

## Próximo passo

- PENDENTE — Após o envio real, Iago informa canal, horário aproximado, confirmação e eventual resposta; então retomar o RevenueRun persistido e registrar `manual-contact` com evidência factual.
