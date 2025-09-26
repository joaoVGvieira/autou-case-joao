import os
import pdfplumber 
import json
import cohere  # 1. NOVO IMPORT
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- INÍCIO DAS MUDANÇAS ---

# 2. CONFIGURAR O CLIENTE DA COHERE
try:
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("Chave COHERE_API_KEY não encontrada no arquivo .env")
    co = cohere.Client(cohere_api_key)
except ValueError as e:
    print(e)
    co = None

def analisar_email_com_ia(conteudo_email):
    """
    Envia o conteúdo do email para a API da Cohere para uma análise simplificada.
    """
    if not co:
        return {"categoria": "Erro de Configuração", "sugestao_resposta": "A chave da API da Cohere não foi configurada corretamente."}

    # --- PROMPT SIMPLIFICADO E MAIS RIGOROSO ---
    prompt = f"""
    Sua única tarefa é analisar o e-mail abaixo e retornar um JSON. Não adicione nenhum texto extra.

    O formato de saída deve ser um JSON válido com apenas duas chaves: "categoria" e "sugestao_resposta".
    - "categoria": Classifique como "Produtivo" APENAS se o e-mail exigir uma ação, resposta ou trabalho. Caso contrário, classifique como "Improdutivo". E-mails de agradecimento, felicitações ou avisos são Improdutivos.
    - "sugestao_resposta": Sugira uma resposta curta e profissional. Para e-mails "Improdutivos", a resposta pode ser "Nenhuma ação necessária.".

    E-mail para análise:
    ---
    {conteudo_email}
    ---

    Exemplo de saída para um e-mail produtivo:
    {{
      "categoria": "Produtivo",
      "sugestao_resposta": "Olá. Recebemos sua solicitação e já estamos verificando. Retornaremos em breve."
    }}

    Exemplo de saída para um e-mail improdutivo:
    {{
      "categoria": "Improdutivo",
      "sugestao_resposta": "Nenhuma ação necessária."
    }}
    """
    
    try:
        response = co.chat(
            model='command-r-plus-08-2024',
            message=prompt,
            temperature=0.2 # Diminuímos ainda mais a "criatividade" para forçar a IA a seguir o formato
        )
        
        texto_resposta = response.text
        return texto_resposta

    except Exception as e:
        print(f"Erro na API da Cohere: {e}")
        return {
            "categoria": "Erro de API",
            "sugestao_resposta": "Não foi possível analisar o e-mail. Verifique sua chave da API da Cohere ou o status do serviço."
        }
# --- FIM DAS MUDANÇAS ---


def extrair_texto_pdf(file_stream):
    """Extrai texto de um arquivo PDF com alta precisão usando pdfplumber."""
    texto = ""
    try:
        # pdfplumber.open() aceita o stream do arquivo diretamente
        with pdfplumber.open(file_stream) as pdf:
            # Itera sobre cada página do PDF
            for page in pdf.pages:
                # Extrai o texto da página, mantendo o layout o máximo possível
                texto_pagina = page.extract_text()
                if texto_pagina:
                    texto += texto_pagina + "\n" # Adiciona uma nova linha entre as páginas
        return texto
    except Exception as e:
        print(f"Erro ao ler PDF com pdfplumber: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        email_texto = request.form.get('email_text')
        email_arquivo = request.files.get('email_file')

        conteudo_final = ""

        if email_arquivo and email_arquivo.filename != '':
            filename = email_arquivo.filename
            if filename.endswith('.txt'):
                conteudo_final = email_arquivo.read().decode('utf-8', errors='ignore')
            elif filename.endswith('.pdf'):
                conteudo_final = extrair_texto_pdf(email_arquivo.stream)
        
        if not conteudo_final and email_texto:
            conteudo_final = email_texto

        if conteudo_final:
            resposta_ia = analisar_email_com_ia(conteudo_final)
            
            if isinstance(resposta_ia, str):
                try:
                    resultado = json.loads(resposta_ia)
                except json.JSONDecodeError:
                    resultado = {
                        "categoria": "Erro de Formato",
                        "sugestao_resposta": f"A IA retornou um formato inválido. Tente novamente. Resposta recebida: {resposta_ia}"
                    }
            else:
                resultado = resposta_ia
        else:
             resultado = {
                    "categoria": "Atenção",
                    "sugestao_resposta": "Por favor, insira o texto de um e-mail ou envie um arquivo .txt ou .pdf."
                }
    
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)