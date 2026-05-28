# Sistema de Gestão Financeira.

Este projeto consiste em uma aplicação de automação e controle financeiro pessoal executada localmente. O objetivo principal é eliminar o trabalho manual que ocorre em frequência com planilhas de controles de gastos, nesse projeto venho construindo um pipeline de dados capaz de pegar faturas e extratos bancários brutos, tratar as informações, e por fim retornar o histórico de gastos de forma padronizada e detalhada.

A ideia central é que o usuário apenas forneça os arquivos exportados pelo banco, deixando para o sistema todo o trabalho pesado de higienização de strings, identificação de parcelas e classificação de modalidades de pagamento.

## Estado Atual do Projeto

Os arquivos deste repositório representam o esqueleto inicial, sendo o motor lógico de processamento de um projeto que estarei continuamente atualizando. 

Atualmente, o pipeline de dados possui estrutura focada no processamento de extratos da instituição **Nubank**. O sistema já é capaz de realizar a triagem automática entre faturas de Cartão de Crédito e extratos de Conta Geral (PIX, Transferências e Débito). A inserção do nome do arquivo alvo ainda é realizada diretamente na estrutura do código de forma manual, contudo o planejamento feito é que para as próximas versões o programa possa estar fazendo esse processo de forma automática, só precisando a inserção do arquivo de dados, outra inserção que deve ser feita é a de integrar uma interface gráfica, contendo tabelas de dados e a adaptação para informações de diferentes bancos.


## Tecnologias e Ferramentas Utilizadas

O sistema foi construído visando performance, separação de responsabilidades e segurança no armazenamento de informações locais.

* **Python 3:** Linguagem base de todo o ecossistema e orquestração do programa.
* **Pandas:** Essencial para a construção do motor ETL. Utilizado para a leitura dos arquivos `.csv`, formatação de matrizes, reordenação de colunas, higienização de textos e aplicação de Expressões Regulares (Regex) para extração inteligente de dados (como numerações de parcelas).
* **SQLite3:** Banco de dados relacional nativo do Python, responsável por persistir as informações limpas em um servidor local com tipagem rigorosa, garantindo a integridade do histórico financeiro do usuário sem a necessidade de conexão com a internet.

## Próximos Passos

* No roadmap planejado tenho os seguintes implementações a fazer:
- Criação de uma Interface Gráfica de Usuário (GUI) utilizando CustomTkinter.
- Desenvolvimento de um painel de controle (Dashboard) com a biblioteca Plotly/Matplotlib para visualização analítica dos gastos.
- Expansão do motor de leitura e Regex para suportar extratos de outras instituições bancárias.
- Mapeamento e categorização inteligente do setor de compras (Alimentação, Transporte, Saúde, etc.) através da análise de palavras-chave nas descrições.
