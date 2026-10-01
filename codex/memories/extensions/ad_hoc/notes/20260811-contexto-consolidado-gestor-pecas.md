# Contexto consolidado do usuário e do Gestor de Peças — 11 de agosto de 2026

## Perfil e forma de colaborar

O usuário é estudante e atua profissionalmente em TI e desenvolvimento. Tem experiência prática com Python, interfaces, bancos de dados, Git/GitHub e IA para programação. Busca sistemas profissionais, estáveis, organizados, seguros e fáceis de manter.

Nas respostas, não inventar fatos. Separar fatos confirmados de deduções e marcar incertezas com `[Não verificado]`, `[Inferência]` ou `[Especulação]`, conforme adequado. Corrigir informação anterior quando ela estiver errada. Para temas atuais, pesquisar fontes atualizadas e priorizar documentação oficial. Evitar perguntas desnecessárias quando o contexto permitir agir. Em temas técnicos, explicar o motivo da solução com detalhe suficiente.

## Projeto Gestor de Peças

O Gestor de Peças é o projeto principal: sistema desktop Python com características de MES para tarefas, OPs, setores produtivos, apontamentos, movimentações, acompanhamento operacional, relatórios, histórico, cadastros, indicadores e integração com dados de produção. Setores incluem Aguardando Dobra, Aguardando Usinagem, Almoxarifado, Dobra, Usinagem e outros fluxos.

A migração de Tkinter/ttk/ttkbootstrap para PySide6/Qt nativo foi concluída tecnicamente. Não criar uma camada de compatibilidade Tkinter-Qt; preservar regras de negócio, serviços, Qlik e funcionalidades. Há cerca de 23 telas em validação visual contra mockups oficiais: a migração funcional/estrutural está concluída, mas a fidelidade visual completa ainda requer validação.

Os mockups em PNG da pasta `Designs aprovados/Telas` e os SVGs de `Designs aprovados/Icons` são a referência visual principal; não substituir o design aprovado por interpretação estética. Diretrizes históricas do design incluem sidebar escura, header branco, fundo claro, painéis brancos, bordas destacadas quando especificadas, e validação de dimensões, espaçamentos, tipografia, ícones, estados e hierarquia. Para trabalhos visuais, abrir e comparar os mockups antes de alterar código e reutilizar SVGs oficiais.

Prioridade de trabalho: funcionamento, regras de negócio, integrações, estabilidade, arquitetura, fidelidade visual, testes e manutenção. O sistema não é um projeto novo: alterar apenas o necessário, evitar reescritas e não modificar regras produtivas, SQL, semântica de dados, Qlik, serviços, OPs, relatórios, histórico, exportações, autenticação ou comportamento operacional sem autorização explícita.

## Arquitetura e integrações

Arquivos e áreas relevantes: `app/launcher.py`, `app/main_window.py`, `app/ui/`, `app/ui/main_window_sections/`, `app/ui/widgets.py`, `app/ui/historico.py`, `app/ui/relatorios.py`, `app/core/`, `app/database/`, `mes/services/` e `qlik/`. A janela principal usa seções/mixins. Serviços produtivos relevantes incluem `task_lookup.py`, `production.py` e `operational_reports.py`; não os alterar arbitrariamente em tarefas visuais.

Qlik Sense/Qlik Engine é integração crítica e deve ser preservada, com autenticação, cookies, Engine API, hypercubes, `qMatrix`, varredura de objetos, transformação e mapeamento de dados. Validar regressões em toda alteração que possa afetá-la. No checkout atual, confirmar os módulos realmente existentes antes de presumir nomes históricos como `explorer.py`, `transform.py` ou `legacy_reader.py`.

O usuário usa Git/GitHub: verificar estado antes de alterar, não assumir commit, não fazer push sem autorização e preservar branches/alterações existentes. No checkout verificado em 2026-08-11, a pasta `.git` estava vazia/incompleta, portanto o estado Git não era consultável até restauração dos metadados ou uso de clone correto.

## Estado atual e correções de informação

O texto de migração fornecido afirma que o banco atual é SQLite e que PostgreSQL é pretendido. Isto conflita com o checkout atual e suas instruções, onde PostgreSQL é o backend oficial, há `app/database/` com pool, migrations e facade, e a documentação descreve PostgreSQL. Tratar a afirmação de SQLite como contexto histórico ou `[Não verificado]` até nova inspeção do ambiente/fluxo ativo; não regredir a arquitetura atual para SQLite sem pedido explícito.

Também há divergência de tipografia: o pacote cita Segoe UI como referência visual histórica, enquanto o checkout atual centraliza Arial como fonte padrão. Para qualquer ajuste visual, verificar `app/core/styles.py` e os mockups atuais em vez de assumir uma das duas fontes.

Validação local em 2026-08-11: Python 3.14.7 pelo interpretador `C:\Python314\python.exe`; compilação e imports principais OK; `python -m unittest discover -s tests` executou 73 testes com sucesso e 11 pulados. Isso não substitui teste manual de Qlik real, PostgreSQL operacional, abertura visual ou fluxo ponta a ponta.

## Problemas e objetivos conhecidos

Houve problemas históricos de layout na Tela Inicial, Consulta Operacional e Tarefas, além de regressões em tentativa anterior de redesign (abas/seleções invisíveis, componentes ausentes, MRO, exportação Excel e atributos `None`). Usar auditoria visual por prioridade P0/P1/P2: comparar tela real e mockup, identificar falta de componentes/layout/estilo, corrigir, abrir a aplicação, verificar regressões e repetir.

Próximos objetivos: concluir validação visual das cerca de 23 telas, eliminar diferenças dos mockups sem perda funcional, consolidar a UI PySide6, evoluir infraestrutura de banco centralizado conforme a arquitetura PostgreSQL verificada, e revisar configuração, segurança, backups e logs quando solicitado.

Ao receber tarefa no projeto: analisar estrutura, dependências e interfaces dos módulos; localizar arquivos ligados ao pedido; alterar apenas o escopo necessário; executar testes aplicáveis; verificar regressões; informar exatamente o que mudou e o que foi efetivamente testado. O arquivo histórico `Gestor de Peças Base Estável.zip` não deve ser presumido disponível sem ser anexado ou acessível no ambiente atual.
