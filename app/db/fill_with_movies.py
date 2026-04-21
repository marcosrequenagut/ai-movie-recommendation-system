import pandas as pd
import ast

from connection import get_connection

# Conection to PostgreSQL database
conn = get_connection()
cur = conn.cursor()

with open("app\db\schema.sql", "r") as f:
    for stmt in f.read().split(";"):
        if stmt.strip():
            cur.execute(stmt)


# Load the CSV
df = pd.read_csv("data_procesing\data\movies_information_with_embeddings_all.csv")

# Transform the "Embedding" column from string to list
df["Embedding"] = df["Embedding"].apply(ast.literal_eval)

# Cast release_year from Float to INT. Remove rows with null release_year 
df["release_year"] = df["release_year"].astype("Int64")
df = df.dropna(subset=["release_year"])


# Insert data into the database
for i, row in df.iterrows():

    embedding = str(row["Embedding"])
    genres = ast.literal_eval(row["genres"]) # Conver a string of array in just an array

    cur.execute("""
        INSERT INTO movies (id, title, content, embedding, adult, original_language, popularity, release_date, release_year, vote_average, genres, weighted_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            row["id"],
            row["title"],
            row["content"],
            embedding,
            row["adult"],
            row["original_language"],
            row["popularity"],
            row["release_date"],
            row["release_year"],
            row["vote_average"],
            genres,
            row["weighted_rating"]
        ))
    
    if i % 100 == 0:
        print(f"Inserted {i} rows")

# Final commit
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully")
