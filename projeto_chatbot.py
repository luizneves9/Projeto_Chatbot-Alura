## -- CASO ABRA NO GOOGLE COLAB -- ##
# 1. Necessário salvar o arquivo .csv na mesma pasta do script (Nas opções a esquerda, tem uma imagem de "pasta", arraste o arquivo para lá ou selecione "Carregar para armazenamento...")
# 2. Necessário incluir e ativar a API_KEY, conforme apresentado em aula
# 3. Necessário a instalação das bibliotecas abaixo
#       pip install dotenv
#       pip install langchain_community
#       pip install langchain_google_genai
#       pip install faiss-cpu
# Abaixo, no código, será necessário a exclusão no código abaixo as referências "#VSCODE>>>>>"" e liberar no código as partes do "#APENAS PARA COLAB<<<<<"

## --- CASO ABRA NO VSCODE -- ##
# 1. Necessário salvar o arquivo .csv na mesma pasta do script
# 2. Necessário salvar os arquivos .env e editá-lo, incluindo sua API_KEY
# 3. Necessário a instalação das bibliotecas abaixo
# pip install dotenv
# pip install langchain_community
# pip install langchain_google_genai
# pip install faiss-cpu

# --- Importação das bibliotecas necessárias ---
from dotenv import load_dotenv # Biblioteca para carregar variáveis de ambiente de um arquivo .env
import os # Biblioteca para interagir com o sistema operacional (caminhos, etc.)
from google import genai # SDK do Google AI para usar o modelo Gemini
from google.genai import types # Tipos específicos da SDK (como configurações de chat)
from google.api_core import exceptions as google_exceptions # Tratar erros da API
from langchain_community.document_loaders import CSVLoader # Carrega dados de um arquivo CSV
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Usado para criar representações vetoriais (embeddings) de texto usando modelos do Google
from langchain_community.vectorstores import FAISS # Biblioteca para criar e gerenciar um vetorstore (banco de dados de vetores) para busca eficiente
from langchain_core.documents import Document # Estrutura básica usada pela Langchain para representar um pedaço de texto e metadados associados.

# --- Configuração de Arquivos e Variáveis de Ambiente ---
# Obtém o diretório onde o script está sendo executado.
script_dir = os.path.dirname(__file__) #VSCODE>>>>>
# Constrói os caminhos completos para os arquivos .env e CSV.
csv_arquivo = os.path.join(script_dir, 'base_empresa.csv') #VSCODE>>>>>
env_arquivo = os.path.join(script_dir, '.env') #VSCODE>>>>>

#### --- Caso execute no Google Colab, precisa excluir as etapas acima (script_dir, csv_arquivo e env_arquivo) e deixar apenas o debaixo (retirar os "#" na frente do código) --- ###
#csv_arquivo = 'base_empresa.csv' #APENAS PARA COLAB<<<<<
#env_arquivo = '.env' #APENAS PARA COLAB<<<<<

try:
    load_dotenv(env_arquivo) # Carrega as variáveis definidas no arquivo .env (API_KEY).
except FileNotFoundError:
    print(f"ERRO: O arquivo .env não foi encontrado em {env_arquivo}")
    print("Certifique-se de que ele está no mesmo diretório do script.")
    exit(1)

api_key = os.environ.get('GOOGLE_API_KEY') # Obtém a chave da API do Google das variáveis de ambiente. #VSCODE>>>>>
#api_key = userdata.get('GOOGLE_API_KEY') #APENAS PARA COLAB<<<<<
if not api_key:
    # Mensagem de erro caso a chave não seja encontrada.
    print('ERRO: A chave GOOGLE_API_KEY não foi encontrada nas variáveis de ambiente.')
    print('Verifique se ela está definida no arquivo .env (ex: GOOGLE_API_KEY=SUA_CHAVE_AQUI).')
    exit(1)

# Configuração para carregar a base de dados CSV, separada por ';'.
try:
    documentos = []
    loader = CSVLoader(
        file_path=csv_arquivo,
        csv_args={'delimiter': ';'},
        encoding='utf-8'
    )
    documentos = loader.load() # Carrega os dados do CSV em objetos Document.
except FileNotFoundError: # Erro específico se o arquivo CSV não for encontrado.
    print(f"ERRO: O arquivo CSV da base de dados não foi encontrado em {csv_arquivo}")
    print("Certifique-se de que ele está no mesmo diretório do script.")
    exit(1)
except Exception as e: # Captura outros erros de leitura ou processamento do CSV (formato, codificação, etc.)
    print(f"ERRO: Não foi possível ler ou processar o arquivo CSV '{csv_arquivo}'.")
    print(f"Verifique se o arquivo existe, o formato (delimitador ';') e a codificação (UTF-8).")
    print(f"Detalhes técnicos do erro: {e}") # Inclui o erro técnico para depuração.
    exit(1)

# Verifica se os documentos foram carregados com sucesso
if not documentos:
    print(f"\nAVISO: Nenhum dado foi carregado do arquivo CSV '{csv_arquivo}'.")
    print("O arquivo pode estar vazio ou conter apenas cabeçalhos.")
    print("O chatbot não terá informações para buscar na base de dados.")
    # Decide sair ou continuar com base vazia. Sair evita erros posteriores ao tentar usar uma base vazia.
    print("Encerrando o programa pois a base de dados está vazia.")
    exit(0)

tipo = 'gemini-1.5-flash' # Define o nome do modelo Gemini a ser usado para o chat.

# Configurando o chat com as instruções para o modelo (persona, regras de resposta, etc.).
chat_config = types.GenerateContentConfig(
    system_instruction= "Você é um assistente pessoal da empresa, especializado em fornecer informações com base nos dados que lhe são apresentados. Responda de forma clara, objetiva e amigável. Se a informação solicitada não estiver no contexto fornecido, diga educadamente que não possui essa informação. Caso não tenha informações na base, e através de pesquisas consiga montar uma resposta que não fuja muito da pergunta."
)

try:
    client = genai.Client(api_key=api_key) # Inicializa o cliente Google AI usando a API key carregada.
    chat = client.chats.create(model=tipo, config=chat_config) #  Cria a instância do chat com o modelo e configuração definidos.
except (google_exceptions.GoogleAPIError, Exception) as e: # Captura erros específicos da API do Google ou outras exceções.
    print(f"\nERRO: Não foi possível conectar ou inicializar o modelo Gemini '{tipo}'.")
    print(f"Verifique sua conexão com a internet, a validade da API key e se o modelo está disponível.")
    print(f"Detalhes técnicos do erro: {e}")
    exit(1)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key) # Cria o objeto que irá gerar os embeddings (representações numéricas) usando o modelo do Google.
vectorstore = FAISS.from_documents(documentos, embeddings) # Cria e organiza a base de dados (vectorstore) em vetores usando os documentos e os embeddings. (caso de erro, verifique se informou o API no arquivo .env)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) # Configura o 'retriever' para buscar na base de dados de vetores (vectorstore).

print("\n--- CHATBOT ALURA INICIADO ---")
print("Digite sua pergunta ou 'sair' para encerrar.")
print("--" * 30)

# Inicia um loop infinito para interagir com o usuário até que ele digite 'sair'.
while True:
    pergunta = str(input('PERGUNTA: ')).strip() # Obtém a entrada do usuário.
    
    if pergunta.lower() == 'sair': # Verifica se o usuário quer sair do programa.
        print('Programa encerrado!')
        break

    if not pergunta:  # Verifica se a entrada do usuário está vazia.
        print('Por favor, digite uma pergunta.')
        continue
    
    try:
        documentos_relevantes: list[Document] = retriever.invoke(pergunta) # Com a pergunta do usuário, o retriever busca e encontra os documentos relevantes na base de dados.
        contexto_formatado = "\n---\n".join([doc.page_content for doc in documentos_relevantes]) # Formata o texto dos documentos relevantes em um bloco único para usar como contexto no prompt.
        # Define o prompt final que será enviado ao modelo Gemini.
        prompt_final = f"""
        Contexto de informações da base de dados:
        {contexto_formatado}

        ---

        Pergunta do usuário: {pergunta}

        ---

        Com base no contexto fornecido acima e na pergunta do usuário, responda de forma útil e concisa.
        - Se a resposta puder ser encontrada no contexto, use as informações fornecidas.
        - Se a resposta não estiver no contexto, mas você tiver conhecimento geral relevante, utilize-o para formar a resposta.
        - Se a resposta não estiver no contexto e você também não tiver conhecimento geral sobre o assunto, informe que a informação específica não foi encontrada na base de dados.
        Mantenha a persona de assistente pessoal da empresa.
        """
        resposta = chat.send_message(prompt_final) # Envia o prompt final para o chat e obtém a resposta do modelo.
        print(f'\nRESPOSTA: {resposta.text}') # Imprime a resposta recebida do modelo.
    except Exception as e: # Captura e imprime qualquer erro que ocorra durante a interação com o chat.
        print(f"Ocorreu um erro durante a interação com o chat: {e}")
    print('\n' + '--'*30)