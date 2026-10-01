---
name: gestor-pecas-github-cicd
description: Gestor de Peças agora sincroniza automaticamente com o GitHub e roda CI (testes + build) a cada push
metadata: 
  node_type: memory
  type: project
  originSessionId: 4989a3e7-84b4-4822-ab62-b81fd6500a72
  modified: 2026-09-27T14:44:53.552Z
---

Desde 18/09/2026 o repositório local está conectado a `https://github.com/iagoluch/gestor-de-pecas` (branch única `master`, definida como default branch; a antiga `main`, com o README/About desatualizados do app desktop PySide6/Qlik Sense, foi apagada).

**Automação em vigor nesta máquina:**
- `.git/hooks/post-commit` dá `git push origin <branch>` sozinho a cada `git commit` (também limpa `desktop.ini` que o OneDrive recria dentro de `.git/refs/`, que corrompia fetch/push).
- `git config --global credential.helper manager` autentica via navegador (Git Credential Manager), sem token manual.
- `.github/workflows/ci.yml` roda a cada push: backend (`python -m unittest discover`, Python 3.14, Postgres 17 de serviço) e frontend (`npm ci && npm run build && npm run test`).

**Why:** o usuário pediu para automatizar a atualização do GitHub, que estava desatualizado (sem remoto configurado até então).

**Gotchas do CI que já custaram investigação (não repetir):**
1. `TEST_DATABASE_URL` do app **exige que o nome do banco contenha `"test"`** (`load_postgres_config`, trava de segurança) — nome do serviço Postgres no CI precisa refletir isso (usei `gestor_pecas_test`).
2. O runner do GitHub Actions usa **UTC** como fuso do SO; a aplicação fixa a sessão PostgreSQL em `America/Sao_Paulo` (`app/database/connection.py`). Sem `TZ=America/Sao_Paulo` no job, `datetime.now()` do Python e `LOCALTIMESTAMP` do Postgres ficam 3h divergentes e `test_sessao_postgresql_usa_o_mesmo_fuso_da_aplicacao` falha. Não é bug de imagem Docker (Alpine vs Debian não fez diferença).
3. `tests/test_quality_inspection.py::QualityPostgresTests` liga a outbox TOTVS de propósito no `setUp` (para observar a obrigação outbound), o que ativa a regra de duração mínima de 60s entre Início/Finalizado. O helper `_concluir_roteiro` e o `QualityInspectionService` do teste agora usam um relógio injetado (`self.clock`) avançado manualmente, em vez de tempo de parede real.
4. `tests/test_stage4c_resource_registry.py::CadastroRealTests` audita o cadastro REAL sincronizado do TOTVS/SigmaNEST do banco TESTE compartilhado — dado que não existe em um banco novo criado só por migration (como o container descartável do CI). A classe agora pula (`SkipTest`) quando `catalogo_recursos_pcfactory` está vazio, em vez de falhar.
5. **(27/09/2026)** `on.push` com só `tags-ignore` faz o GitHub ignorar todo push de branch: o CI ficou desligado no master de 20/09 a 27/09 sem ninguém notar. Use `branches: ["**"]`, que já exclui tags.
6. **(27/09/2026)** A trava `506a92f` exige `GESTOR_EXPECTED_DATABASE` quando `testing=True`; sem ela no env do job, ~193 testes dão `DatabaseConfigurationError`.

**How to apply:** se o CI voltar a falhar em algo parecido com esses 4 padrões, a causa provavelmente já é conhecida — não repetir a investigação do zero. Ver também [[repo-protheus-advpl-separado]] para o achado de segurança (senha real do TOTVS) encontrado durante esse trabalho.
