---
name: validacao-integrada
description: Regra para rodadas de validação integrada/simulação prolongada no Gestor de Peças (ex. Wave 6I) — observar e classificar antes de corrigir código. Use quando a tarefa for rodar uma simulação de fábrica virtual, soak test, ou qualquer validação ponta a ponta do sistema.
---

# Validação integrada (Wave 6I e futuras rodadas)

Este projeto roda periodicamente uma "fábrica virtual observável" (`simulacao/`, script `scripts/run_simulacao_industrial.py`) para validar várias Waves de desenvolvimento já implementadas rodando juntas sob carga prolongada.

## Regra central: observar e classificar primeiro, decidir depois
O objetivo de uma rodada de validação integrada **não é** desenvolver ou corrigir — é gerar evidência real de como o sistema se comporta com tudo junto. Se você corrigir código no meio da rodada, ou logo que encontra algo estranho, a rodada deixa de ser validação e vira uma wave de desenvolvimento disfarçada, o que o dono do projeto quer evitar explicitamente.

**Portanto, durante e logo após rodar a simulação:**
- **Não edite nenhum arquivo de código do sistema** (fora do simulador) com base no que a rodada mostrar.
- Se o **simulador em si** tiver um bug óbvio impedindo a simulação de rodar (ex.: erro de sintaxe, chamada de API quebrada por mudança de contrato), aí sim é razoável corrigir — o simulador é ferramenta, não é o sistema sendo validado.
- Se encontrar algo que parece bug do **sistema real** (backend/frontend), **registre** com detalhe (arquivo, sintoma, evidência do relatório/log) e devolva para decisão humana. Não abra PR, não edite, não "aproveite que já está ali".
- Falso positivo do detector da simulação (ex.: um estado novo que o comparador ainda não reconhece) é diferente de bug do sistema — também não corrigir automaticamente sem pedir, só relatar.

## Ao final de uma rodada, sempre entregue
1. Caminho do relatório gerado (`simulation_runs/<timestamp>/report*.md`).
2. Resumo objetivo: volume de eventos, OPs finalizadas, bloqueios esperados, erros 5xx/timeout.
3. Status de cada cobertura nova relevante à rodada (o que estava sendo validado desta vez).
4. Qualquer achado fora do esperado, com evidência (trecho de log/relatório), sem aplicar correção.

## Infra conhecida deste projeto (economize tempo, não redescubra)
- Use sempre `.venv\Scripts\python.exe`, nunca o Python do sistema (faltam pacotes como `psycopg` fora do venv).
- A porta 8001 (padrão de `config/simulacao_industrial.json`) tem uma pendência de infraestrutura conhecida nesta máquina: o backend WSL2 do Docker Desktop deixa uma regra de encaminhamento de porta presa nela, com um PID que não existe mais no Windows mas segue "ocupando" a porta. Não é corrigível por `taskkill`/`Stop-Process` local — não perca tempo tentando matar esse processo. Use portas alternativas via `--api-port`/`--observatory-port` do script (confirme antes que estão livres com `netstat -ano | findstr ":<porta>"`).
