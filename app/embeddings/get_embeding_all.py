import requests
import numpy as np
import pandas as pd

def get_embedding(text):

    response = requests.post(
        "http://ollama:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    print(response.status_code, response.text)  # DEBUG

    response.raise_for_status()

    return response.json()["embedding"]

def cosine_similarity(vec1, vec2):
    a = np.array(vec1)
    b = np.array(vec2)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))



path = "data_procesing\movies_information.csv"

df = pd.read_csv(path)

dict_movie_embeddings = {}

i=0
for _, row in df.iterrows():
    content = row["content"]
    embedding = get_embedding(content)
    dict_movie_embeddings[row["id"]] = embedding
    print(f"Embedding {i}")
    i += 1

df["Embedding"] = df["id"].map(dict_movie_embeddings)

df.to_csv("data_procesing\movies_information_with_embeddings_all.csv", index=False)
