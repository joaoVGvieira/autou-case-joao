# AutoU - Case Prático: Classificador Inteligente de E-mails

Este projeto é a solução para o case prático do processo seletivo da AutoU. Trata-se de uma aplicação web que utiliza a API da Cohere para classificar e-mails como "Produtivos" ou "Improdutivos" e sugerir respostas automáticas.

**Link da Aplicação:** https://autou-case-joao-mol9.onrender.com/

## Funcionalidades

- Classificação de e-mails em **Produtivo** ou **Improdutivo**.
- Geração de **respostas automáticas** contextuais.
- Interface para **colar texto** ou fazer **upload de arquivos .txt e .pdf**.
- Componente de upload moderno com suporte a "arrastar e soltar".
- Botão para **copiar a resposta sugerida** com um clique.

## Tecnologias Utilizadas

- **Backend:** Python com Flask
- **Inteligência Artificial:** API da Cohere
- **Frontend:** HTML5, CSS3 e JavaScript
- **Extração de PDF:** Biblioteca Pdfplumber
- **Hospedagem:** Render

## Como Rodar Localmente

1.  **Clone o repositório:**
    `git clone [link do seu repositório]`
2.  **Instale as dependências:**
    `pip install -r requirements.txt`
3.  **Configure as variáveis de ambiente:**
    - Crie um arquivo `.env` na raiz do projeto.
    - Adicione sua chave da API: `COHERE_API_KEY="sua_chave_aqui"`
4.  **Execute a aplicação:**
    `python app.py`
5.  Acesse `http://127.0.0.1:5000` no seu navegador.
