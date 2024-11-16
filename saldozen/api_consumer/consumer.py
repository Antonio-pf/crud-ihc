# app/api_consumer/consumer.py
import requests

def get_api_data(url):
    """Função para fazer uma requisição GET e retornar os dados JSON."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.json()  
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None
