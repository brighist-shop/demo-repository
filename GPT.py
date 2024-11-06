import csv
import os
import re

CACHE_FILE = 'agent_cache.csv'

# Função para carregar o cache do arquivo CSV em um dicionário
def load_cache():
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 3:
                    termo, pergunta, resposta = row
                    cache[termo] = (pergunta, resposta)
    return cache

# Função para salvar uma nova entrada no cache (CSV)
def save_to_cache(termo, pergunta, resposta):
    with open(CACHE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([termo, pergunta, resposta])

# Função para extrair o termo principal da pergunta usando regex para capturar palavras significativas
def extract_terms(pergunta):
    # Remove caracteres especiais e mantém apenas palavras
    terms = re.findall(r'\b\w+\b', pergunta.lower())
    return terms

# Função principal para buscar no cache ou consultar o banco de dados
def query_agent(pergunta):
    # Extrair termos principais da pergunta
    termos = extract_terms(pergunta)
    
    # Carregar o cache do CSV
    cache = load_cache()

    # Verificar se algum termo já está no cache
    for termo in termos:
        if termo in cache:
            print(f"Resultado encontrado no cache para o termo '{termo}'.")
            return cache[termo][1]  # Retorna a resposta do cache associada ao termo

    # Se não estiver no cache, faz a consulta no banco de dados
    resposta = consult_database(pergunta)
    if resposta:
        # Salva a nova pergunta e resposta no cache para cada termo encontrado
        for termo in termos:
            save_to_cache(termo, pergunta, resposta)
    else:
        resposta = "Nenhuma informação encontrada no banco de dados."
    
    return resposta

# Simula a consulta no banco de dados (substitua com a sua lógica de BD)
def consult_database(pergunta):
    # Exemplo fictício de respostas do banco de dados
    database = {
        "teste.docx": "O documento teste.docx contém informações sobre o projeto.",
        "relatório": "O relatório anual está salvo em relatório_2023.docx.",
        "manual": "O manual de instruções está em manual_uso.docx."
    }
    # Tenta encontrar uma resposta com base nas palavras-chave conhecidas
    termos = extract_terms(pergunta)
    for termo in termos:
        if termo in database:
            return database[termo]
    return None

# Exemplo de uso
pergunta1 = "Tagra o documento teste.docx"
resposta1 = query_agent(pergunta1)
print("Resposta:", resposta1)

pergunta2 = "O que tem dentro do teste.docx"
resposta2 = query_agent(pergunta2)
print("Resposta:", resposta2)

pergunta3 = "Preciso do relatório anual"
resposta3 = query_agent(pergunta3)
print("Resposta:", resposta3)

pergunta4 = "Onde encontro o manual de instruções?"
resposta4 = query_agent(pergunta4)
print("Resposta:", resposta4)
