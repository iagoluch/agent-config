# Andon Web: TV e gestores

- A rota `/andon` pertence ao usuário dedicado `andon` e será usada na TV da fábrica.
- A visão da TV deve mostrar somente os cartões do Andon: sem cabeçalho, logo, resumo da fábrica ou barras superiores da aplicação.
- Na TV, preservar todas as informações dos cartões, remover barras horizontais longas dos indicadores, priorizar legibilidade e manter os 24 recursos sem rolagem em Full HD.
- Ordem visual obrigatória dos setores: Corte, Dobra, Usinagem, Serra, Pintura e Solda.
- Valores fictícios são permitidos somente no modo de simulação e não podem ser persistidos como dados produtivos.
- Gestores acessam o mesmo Andon por uma sub-aba própria em `/inicio/andon`, dentro da navegação gerencial e com layout adequado ao monitor do PC.
- As duas visões devem consumir o mesmo endpoint e os mesmos dados; a apresentação gerencial não pode alterar a visão da TV.
