import pandas as pd
import numpy as np
import ast
from get_embeding import get_embedding, cosine_similarity


df = pd.read_csv("data_procesing\movies_information_with_embeddings.csv")
df["Embedding"] = df["Embedding"].apply(ast.literal_eval)
dict_movie_embeddings = dict(zip(df["id"], df["Embedding"]))

query = "A movie about a young wizard who discovers his magical heritage and attends a school of witchcraft and wizardry."

def get_reccomended_movies(query, top_k, dict_movie_embeddings=dict_movie_embeddings, df=df):
    
    query_embedding = get_embedding(query)

    old_similarity = 0
    similarity_list = []
    i=0
    for id, embedding in dict_movie_embeddings.items():

        similarity = cosine_similarity(query_embedding, embedding)
        print(f"Similarity {i} calculated")
        similarity_list.append((similarity, id))

        # Order by similarity from highest to lowest
        similarity_list.sort(reverse=True, key=lambda x: x[0])

        # Take the top k most similar movies
        top_k_similarity = similarity_list[:top_k]

        # Extract the ids of the most similar movies
        id_most_similar_movie = [id for _, id in top_k_similarity]
        values_similarity = [similarity for similarity, _ in top_k_similarity]

        # Filter the dataframe to get the information of the most similar movies
        df_result = df[df["id"].isin(id_most_similar_movie)]

        # Create a new column with the similarity values
        df_result['similarity'] = df_result['id'].map(dict(zip(id_most_similar_movie, values_similarity)))

        i += 1

    return df_result


print("Recommended movies:")
print("\n")
df_result = get_reccomended_movies(query, 10, dict_movie_embeddings, df)
print(df_result[["title", "similarity"]].sort_values(by="similarity", ascending=False))