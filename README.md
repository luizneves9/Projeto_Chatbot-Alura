# Projeto - Imersao Alura

- Como fazer uma IA responder perguntas usando uma base de dados sua?
- Este projeto é um chatbot que usa o Google Gemini e busca vetorial para encontrar informações nos dados.
- Usamos dados da ALURA como exemplo. Essa base funciona para criar bots que respondem usando dados internos ou arquivos de texto.

- Utilização de bibliotecas: google, os, langchain

# Funcionamento do projeto

### Como Funciona (Visão Geral)

1.  O chatbot carrega dados de um arquivo CSV (como `base_empresa.csv`).
2.  Ele cria representações numéricas (embeddings) desses dados usando um modelo do Google.
3.  Esses embeddings são organizados em uma base vetorial (FAISS) para permitir buscas rápidas.
4.  Quando o usuário faz uma pergunta, o chatbot a transforma em um embedding e busca na base vetorial os trechos de dados mais relevantes.
5.  Os trechos encontrados são enviados ao modelo Google Gemini como contexto, junto com a pergunta original.
6.  O modelo Gemini gera a resposta com base nesse contexto.

### Bibliotecas Utilizadas

As principais bibliotecas utilizadas neste projeto incluem:

* `google-generativeai` (SDK do Google AI para interagir com Gemini)
* `python-dotenv` (Para carregar a chave de API de um arquivo .env)
* `langchain-community` (Para carregar dados CSV e usar o FAISS Vectorstore)
* `langchain-google-genai` (Para gerar embeddings usando modelos do Google)
* `faiss-cpu` (Dependência para a base vetorial FAISS)
* `os` (Para lidar com caminhos de arquivo)

---

## Configuração e Instalação para VSCODE

Para rodar este projeto localmente, siga os passos abaixo:

1.  Certifique-se de ter **Python 3.7+** instalado.
2.  Clone este repositório para o seu ambiente local
3.  Instale as dependências do projeto. É recomendado usar um ambiente virtual (`venv`):
    ```bash
    python -m venv venv
    source venv/bin/activate # No Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    **(Nota:** Você precisará criar um arquivo `requirements.txt` contendo as bibliotecas listadas acima, ou instalá-las manualmente via `pip install google-generativeai python-dotenv langchain-community langchain-google-genai faiss-cpu`.)
4.  Obtenha uma chave de API do **Google Gemini** (através do [Google AI Studio](https://aistudio.google.com/)).
5.  Crie um arquivo na raiz do projeto chamado `.env` e adicione sua chave de API nele:
    ```dotenv
    GOOGLE_API_KEY=SUA_CHAVE_DE_API_AQUI
    ```
    Substitua `SUA_CHAVE_DE_API_AQUI` pela chave que você obteve.
6.  Adicione sua base de dados. O script foi configurado para ler um arquivo CSV chamado `base_empresa.csv` no mesmo diretório do script principal. O arquivo deve usar `;` como delimitador. Adapte-o com as informações que você deseja que o chatbot utilize (formato CHAVE;INFORMAÇÃO ou similar, dependendo de como você quer que o `CSVLoader` da Langchain o interprete).

### Como Executar

Com as configurações acima prontas, execute o script Python principal:

---

## Configuração e Execução no Google Colab

Siga estes passos no seu notebook Colab:

1.  **Instalar Bibliotecas:**
    Crie e execute uma célula de código com o seguinte comando para instalar todas as dependências:
    ```bash
    !pip install google-generativeai python-dotenv langchain-community langchain-google-genai faiss-cpu
    ```

2.  **Configurar a Chave de API:**
    É **altamente recomendado** usar o recurso "Secrets" do Colab:
    * Clique no ícone de chave (🔑) na barra lateral esquerda.
    * Adicione um novo Secret com o nome `GOOGLE_API_KEY` e cole sua chave de API como valor.
    * Certifique-se de que está ativado para este notebook.

3.  **Carregar o Arquivo CSV da Base de Dados:**
    * No painel esquerdo do Colab (ícone de pasta 📁), clique no ícone de upload (⬆️).
    * Selecione e faça upload do seu arquivo `base_empresa.csv` (ou o nome que você deu à sua base). Ele será carregado para o diretório `/content/` da sessão. Certifique-se de que o código do chatbot aponta para o nome correto do arquivo.

4.  **Colar e Executar o Código do Chatbot:**
    * Cole o código Python completo do seu chatbot em uma nova célula de código no notebook.

5. Abaixo, no código, será necessário a exclusão das linhas que contenham "#VSCODE" e liberar no código as partes do "#COLAB" (Utilizar as teclas CTRL + F)
   * Execute a celula

7.  **Interagir:**
    * Após a inicialização, você verá um campo de input na área de output da célula.
    * Digite suas perguntas e pressione Enter.
    * Digite 'sair' para encerrar o chatbot.

