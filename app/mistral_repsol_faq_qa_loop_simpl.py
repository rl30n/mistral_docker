#!/usr/bin/env python3
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="Connecting to 'https://localhost:9200' using TLS with verify_certs=False is insecure")

# Requisitos:
# pip install elasticsearch requests sentence-transformers numpy

from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import requests
import time

# Configuración de Elasticsearch
es = Elasticsearch(
    "https://es01:9200",
    basic_auth=("elastic", "changeme"),
    verify_certs=False
)

INDEX = "faq-repsol-embeddings"  # Actualiza si reindexas
TEXT_FIELD = "body_content"
EMBEDDING_FIELD = "embedding"

# Cargar modelo de embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

print("🤖 Pregunta sobre las FAQs de Repsol. Escribe 'salir' para terminar.")


def main(query: str) -> str:

    # Generar vector de consulta
    query_vector = model.encode(query).tolist()

    # Consulta semántica
    search_body = {
        "size": 3,
        "knn": {
            "field": EMBEDDING_FIELD,
            "k": 3,
            "num_candidates": 100,
            "query_vector": query_vector
        }
    }

    start_time = time.time()
    res = es.search(index=INDEX, body=search_body)
    docs = res["hits"]["hits"]

    context = "\n\n".join(f"Título: {doc['_source'].get('title', 'Sin título')}\nContenido: {doc['_source'].get(TEXT_FIELD, '')}" for doc in docs)
    ids = [doc["_id"] for doc in docs]

    prompt = f"""Eres un asistente inteligente que responde en base a las FAQs de Repsol.
A continuación tienes un conjunto de fragmentos extraídos de su sitio web:

{context}

Pregunta: {query}
Respuesta:"""

    # Enviar a Mistral
    response = requests.post("http://mistral:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    end_time = time.time()
    duration = end_time - start_time

    print("\n🤖 Respuesta generada por Elastic (con la IA Mistral):\n")
    print(response.json()["response"])
    print("\n")
    print("*****************************")
    print(f"📄 IDs de documentos utilizados: {ids}")
    print(f"⏱ Tiempo total de generación: {duration:.2f} segundos\n")
    print("*****************************")

    try:
        return response.json()["response"]
    except (KeyError, IndexError, TypeError):
        return "No se pudo interpretar la respuesta del modelo."
