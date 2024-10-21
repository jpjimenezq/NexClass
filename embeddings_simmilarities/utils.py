import os
import pickle
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import numpy as np

_ = load_dotenv('api_keys.env')
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get('openai_apikey'),
)

def generate_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return embedding

def save_embedding_to_binary(embedding):
    return pickle.dumps(embedding)

def load_embedding_from_binary(binary_embedding):
    return pickle.loads(binary_embedding)

def calcular_similitud(embedding_aspirante, embedding_empleo):
    dot_product = np.dot(embedding_aspirante, embedding_empleo)
    norm_aspirante = np.linalg.norm(embedding_aspirante)
    norm_empleo = np.linalg.norm(embedding_empleo)
    return dot_product / (norm_aspirante * norm_empleo)
