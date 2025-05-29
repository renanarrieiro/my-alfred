import google.generativeai as genai

genai.configure(api_key=API_KEY)

def get_models():
    print("Verificando modelos disponíveis...")
    try:
        for m in genai.list_models():
            # Filtra apenas os modelos que suportam a geração de conteúdo (textos)
            if "generateContent" in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
        print("Por favor, verifique sua chave API e sua conexão com a internet.")
        exit() # Sai do programa se não conseguir listar os modelos

    print("\n") # Adiciona uma linha em branco para melhor visualização

def define_model(model_name):
    return genai.GenerativeModel(model_name=model_name)

def ask_to_model(gemini):
    question = "Quantos títulos mundiais o Corinthians tem?"
    print(f"Perguntando ao Gemini Pro: '{question}'")

    response = gemini.generate_content(contents=question)
    print("\nResposta do Gemini Pro:")
    print(response.text)

# get_models()
ask_to_model(define_model(GEMINI_MODEL_NAME))