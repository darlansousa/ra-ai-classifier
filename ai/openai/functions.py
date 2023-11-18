import os
from openai import OpenAI
from ai.model.complaint_input import ComplaintInput

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze(complaint_input: ComplaintInput):
    text = f"""{complaint_input.title}. {complaint_input.description}"""
    prompt = f"""
    Essa é uma tarefa de análise e classificação de texto
    Por favor classifique o texto a seguir com uma das seguintes categorias [ 
    Economia,
    Baixa injeção de energia,
    Multa/Cancelamento,
    Dúvida,
    Inocnsistência na venda,
    Acesso ao portal/app,
    Programa de pontos,
    Cobrança indevida,
    Prazo conexão excedido,
    Outros]: 

    {text}
    
    Trazer apenas nome da categoria:
    """
    try:
        response = client.completions.create(
            model=os.getenv("OPENAI_API_MODEL"),
            prompt=prompt,
            max_tokens=30,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return e



