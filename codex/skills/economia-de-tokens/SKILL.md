---
name: economia-de-tokens
description: Política de execução eficiente do dono deste projeto (Gestor de Peças) — priorizar ação sobre análise excessiva, validação proporcional ao risco, sem suítes completas por padrão. Use isto em qualquer tarefa de código, investigação, debug ou validação neste repositório.
---

# Economia de tokens e execução pragmática

Este projeto tem um dono que prioriza **resultado prático, velocidade de execução e economia de tokens**, mantendo qualidade técnica. Aplique estas regras em toda tarefa de código, análise ou simulação neste repositório.

## 1. Não fazer análise excessiva antes de executar
Faça só a análise necessária para entender o que precisa mudar, localizar os arquivos relevantes e identificar dependências/riscos diretamente ligados à tarefa. Depois disso, **comece a implementação imediatamente**. Não gaste a maior parte do orçamento de tokens analisando possibilidades que provavelmente não serão usadas.

## 2. Análise proporcional à tarefa
- Tarefa simples/localizada: localizar → alterar → validação rápida.
- Tarefa moderada: inspecionar os arquivos afetados → implementar → validar os fluxos diretamente relacionados.
- Tarefa complexa/crítica: análise mais profunda só onde ela realmente reduz risco.

Não aplique o nível de investigação de uma refatoração crítica a uma alteração simples.

## 3. Evitar "suíte completa" por padrão
Não execute automaticamente toda a suíte de testes, todos os linters, builds completos ou análises completas do repositório. Valide **só o que foi afetado pela mudança**. Rodar a suíte completa só quando: (1) a mudança tiver impacto transversal significativo; (2) houver evidência de regressão; (3) for pedido explicitamente; (4) a validação localizada não for suficiente.

## 4. Não testar infinitamente
Depois de uma correção bem implementada e validada, não fique procurando problemas hipotéticos indefinidamente. Sem ciclo de "analisar → achar possibilidade → testar → analisar de novo" sem evidência concreta. Com evidência suficiente de que o requisito foi atendido, **encerre a tarefa**.

## 5. Ordem padrão
**Entender → localizar → implementar → validar o necessário → entregar.**
Não: "entender → mapear todo o sistema → auditar arquitetura → rodar todos os testes → investigar hipóteses → só então implementar."

## 6. Comunicação enxuta
Relate apenas: o que foi alterado, problemas relevantes encontrados, validação realizada, e qualquer limitação/risco importante. Sem narrar cada arquivo lido, sem justificativas repetitivas, sem descrição detalhada de testes triviais.

## 7. Correções devem ser diretas
Quando pedirem para corrigir algo com causa já clara: corrija, valide, entregue. Só aprofunde a investigação se a correção não funcionar ou houver risco técnico relevante.

## 8. Regra de prioridade
Entre análise/teste adicional de baixo valor e a execução da tarefa pedida, **priorize a execução**, desde que haja informação suficiente para fazê-la com segurança razoável.
