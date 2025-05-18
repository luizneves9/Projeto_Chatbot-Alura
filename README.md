# Imersao_Alura

- Como fazer uma IA responder perguntas usando uma base de dados sua?
- Este projeto é um chatbot que usa o Google Gemini e busca vetorial para encontrar informações nos dados.
- Usamos dados da ALURA como exemplo. Essa base funciona para criar bots que respondem usando dados internos ou arquivos de texto.

- Utilização de bibliotecas: google, os, langchain

# Utilização do código dentro do Google Colab

1. Necessário salvar o arquivo .csv na mesma pasta do script (Nas opções a esquerda, tem uma imagem de "pasta", arraste o arquivo para lá ou selecione "Carregar para armazenamento...")
2. Necessário incluir e ativar a API_KEY, conforme apresentado em aula
3. Necessário a instalação das bibliotecas abaixo
-     !pip install langchain_community
      !pip install langchain_google_genai
      !pip install faiss-cpu
4. Abaixo, no código, será necessário a exclusão no código abaixo as referências "#VSCODE"" e liberar no código as partes do "#COLAB"

# Utilização do código dentro do VS CODE

1. Necessário salvar o arquivo .csv na mesma pasta do script
2. Necessário salvar os arquivos .env e editá-lo, incluindo sua API_KEY
3. Necessário a instalação das bibliotecas abaixo
- 	  pip install dotenv
      pip install langchain_community
      pip install langchain_google_genai
      pip install faiss-cpu
