# Claude Brain V3

Este diretório é a memória operacional do Claude Code.

## Princípios

- Fatos confirmados são separados de hipóteses.
- Memória deve ser pequena, útil e atualizada incrementalmente.
- Não registrar detalhes banais ou cada mensagem.
- Priorizar contexto que evita redescoberta: arquitetura, decisões, padrões,
  problemas conhecidos e estado de projetos.
- A memória não substitui o código nem o CLAUDE.md.

## Arquivos

- `context/` — preferências e regras estáveis.
- `projects/` — estado por projeto.
- `decisions/` — decisões arquiteturais/técnicas.
- `state/` — estado operacional curto.
- `sessions/` — índices/resumos de sessões.
- `logs/` — logs técnicos mínimos.
- `hooks/` — automação do cérebro.
