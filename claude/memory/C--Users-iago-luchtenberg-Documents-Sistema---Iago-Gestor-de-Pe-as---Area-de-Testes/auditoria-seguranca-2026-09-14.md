---
name: auditoria-seguranca-2026-09-14
description: "Auditoria de segurança completa (OWASP) rodada em 2026-09-14 — 1 crítico corrigido (SOAP TOTVS sem auth exposto via túnel Cloudflare), pendências reais que precisam de decisão do usuário"
metadata: 
  node_type: memory
  type: project
  originSessionId: c825e26a-1802-470e-982d-dc79a1d604c4
  modified: 2026-09-14T03:10:50.416Z
---

Relatório completo: `docs/AUDITORIA_SEGURANCA_2026-09-14.md`.

**CRÍTICO corrigido**: `POST /PcfIntegService` (receptor SOAP do TOTVS) não tinha nenhum gate de autenticação e uma mensagem aceita grava OP no banco e comita. Isso vira crítico porque `iniciar_sistema_teste_cloudflare.py` publica o sistema num túnel Cloudflare público e o `.env` já tem esse hostname em `GESTOR_WEB_ALLOWED_HOSTS` com `GESTOR_TOTVS_SOAP_ENABLED=true` — ou seja, qualquer um na internet podia gravar OPs fantasma no TESTE via esse túnel. Corrigido em `backend/integrations/totvs_soap.py:30` (`_arrived_through_public_host`): recusa 403 quando a requisição chega pelo hostname público do túnel, aceita normalmente pela LAN.

**ALTO corrigido**: login do Dev Observatory (criado nesta mesma sessão, 2026-09-13) não tinha freio de tentativa — credencial única guardando stack trace/PostgreSQL/leitura do REAL, alcançável pelo mesmo túnel, adivinhação ilimitada. Agora bloqueia por IP após 5 falhas / 300s. Junto veio um bug sério achado de brinde: `secrets.compare_digest` derrubava o login com 500 em qualquer senha acentuada (teria quebrado o login para sempre se a senha real tivesse acento) — corrigido comparando bytes UTF-8.

**Pendências que precisam da SUA decisão (não corrigidas de propósito):**
1. **Login principal (`/api/v1/auth/login`) também sem freio de tentativa**, no mesmo túnel exposto. Não foi travado de propósito: bloquear login pode impedir um operador de apontar produção no chão de fábrica se errar a senha num terminal compartilhado. Sugestão do relatório: atraso progressivo por IP+usuário em vez de bloqueio total.
2. **IDOR na Qualidade**: `registrar_peca`/`finalizar_inspecao` não validam que o `inspecao_id` pertence ao setor do operador (só `abrir_inspecao` valida). Um operador podia trocar o ID e escrever na inspeção de outro setor. Não corrigido porque a tabela `qualidade_inspecoes` não guarda o setor de origem — precisa de uma migração de schema, não é fix de uma linha.
3. **`.env` não define `GESTOR_WEB_SESSION_SECRET` nem `GESTOR_DEVOBS_SESSION_SECRET`** — ambos os logins usam segredo efêmero gerado a cada boot, então toda sessão (principal e Dev Observatory) cai sempre que o processo da API reinicia. Fácil de resolver: gerar e colar os dois valores no `.env`.

**Verificado como correto (não precisa mexer)**: SQL 100% parametrizado, sem subprocess/eval/pickle, XXE bloqueado com defusedxml, path traversal do `/reports/{name}` protegido corretamente, CSRF em todas as rotas de escrita, PBKDF2-SHA256 600k, sem dangerouslySetInnerHTML, garantia de somente-leitura do REAL sem desvio encontrado. `pip-audit`: 0 vulnerabilidades em 36 pacotes. `npm audit`: 2 moderadas, ambas devDependency do `vitest` (correção é major breaking, não aplicado).

**Why:** pedido explícito do usuário em 2026-09-14 ("pente fino na segurança... kali linux e outros") — esclarecido que não há ferramentas ofensivas reais disponíveis nesse ambiente; foi feita auditoria de código nível OWASP + testes de fronteira pontuais e não-destrutivos contra o TEST local.

**How to apply:** quando o usuário quiser resolver as 3 pendências acima, ir direto aos arquivos citados — não precisa reabrir a auditoria inteira. Ver também [[pente-fino-2026-09-14]] para a auditoria geral de qualidade de código que rodou em paralelo.
