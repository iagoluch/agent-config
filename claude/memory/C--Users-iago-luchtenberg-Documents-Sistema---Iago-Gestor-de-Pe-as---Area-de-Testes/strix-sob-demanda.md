---
name: strix-sob-demanda
description: "Strix (pentest com agentes) instalado via uv, uso SÓ sob demanda contra alvo próprio; launcher com Nemotron 3 Ultra free da NVIDIA, chave via env, nunca hardcoded."
metadata:
  node_type: memory
  type: project
  originSessionId: 8393514e-8576-4c7e-8b96-4804691ed7bf
  modified: 2026-09-30T14:48:55.859Z
---

Instalado em 29/09/2026 com `uv tool install strix-agent` (v1.6.2; binário `strix` em `~/.local/bin`). Precisa do Docker (roda o alvo num sandbox). NADA automático: sem hook, sem CI, sem autostart — decisão do usuário.

Launcher: `~/.local/bin/strix-nemotron.sh`. Fixa o provider NVIDIA NIM via LiteLLM (`STRIX_LLM=nvidia_nim/nvidia/nemotron-3-ultra-550b-a55b`, `LLM_API_BASE=https://integrate.api.nvidia.com/v1`) e `--max-budget 5`. A chave NÃO é hardcoded: exige `NVIDIA_API_KEY` (nvapi-...) exportada na hora. A chave do Goose vive no keyring e não é reutilizada aqui de propósito.

**Why:** Strix ataca de verdade (dual-use); só contra sistema próprio (app TEST local, este repo). O usuário quis o Nemotron free para não gastar Claude/pago. Tier free tem rate limit agressivo → o pentest faz muitas chamadas → esperar lentidão; teto de custo por padrão.
**How to apply:** rodar manualmente, ex.: `NVIDIA_API_KEY=nvapi-... bash ~/.local/bin/strix-nemotron.sh -t http://127.0.0.1:8001 --instruction "..."`. App TEST roda na porta **8001**, não 8000. Nunca apontar para produção nem para o REAL. Ver [[ferramentas-rejeitadas-triagem-29-09-2026]].

**Gotcha 30/09/2026 — trampoline do uv quebrado:** `strix --version`/`--help` dava `error: uv trampoline failed to canonicalize script path` mesmo com o binário presente. Causa: `uv tool uninstall strix-agent` acusou "not installed" (registro do uv dessincronizado do disco) e o `uv tool install strix-agent` seguinte reinstalou os 89 pacotes mas falhou no último passo (`error: Executable already exists: strix.exe`), deixando o `.exe` antigo/quebrado intocado. Fix: `uv tool install --force strix-agent` (sobrescreve o trampoline). Rodar sempre no Git Bash real do usuário (não custa reproduzir aqui via Bash tool antes, mas o fix precisa rodar no terminal dele).
Primeira execução real baixa a imagem Docker `ghcr.io/usestrix/strix-sandbox:1.3.0` (só uma vez, ~33 layers) antes de começar o pentest.
