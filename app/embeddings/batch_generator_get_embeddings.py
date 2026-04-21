import pandas as pd
from app.embeddings.client import get_embedding

DATA_PATH = "data_procesing/movies_information.csv"
OUTPUT_PATH = "data_procesing/movies_information_with_embeddings_all.csv"


def generate_embeddings():

    df = pd.read_csv(DATA_PATH)

    embeddings = []

    for i, row in df.iterrows():
        embedding = get_embedding(row["content"])
        embeddings.append(embedding)
        print(f"Embedding {i}")

    df["Embedding"] = embeddings

    df.to_csv(OUTPUT_PATH, index=False)

    print("Embeddings generated successfully")


if __name__ == "__main__":
    generate_embeddings()