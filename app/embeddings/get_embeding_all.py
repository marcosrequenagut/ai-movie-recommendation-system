import requests
import numpy as np
import pandas as pd

def get_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    #print(response.status_code, response.text)  # DEBUG

    response.raise_for_status()

    return response.json()["embedding"]




path = "data_procesing\data\movies_information.csv"

df = pd.read_csv(path)

dict_movie_embeddings = {}

i=0
for _, row in df.iterrows():
    content = row["content"]
    embedding = get_embedding(content)
    dict_movie_embeddings[row["id"]] = embedding
    if i%100 == 0:
        print(f"Embedding {i}")
    i += 1

df["Embedding"] = df["id"].map(dict_movie_embeddings)

df.to_csv("data_procesing\movies_information_with_embeddings_all.csv", index=False)
