import pandas as pd
import ast

from connection import get_connection

# Conection to PostgreSQL database
conn = get_connection()
cur = conn.cursor()

# Load the CSV
df = pd.read_csv("data_procesing\movies_information_with_embeddings.csv")

# Transform the "Embedding" column from string to list
df["Embedding"] = df["Embedding"].apply(ast.literal_eval)

# Insert data into the database
for i, row in df.iterrows():
    cur.execute("""
        INSERT INTO movies_with_embeddings (id, title, content, embedding)
        VALUES (%s, %s, %s, %s)""",
        (
            row["id"],
            row["title"],
            row["content"],
            row["Embedding"]
        ))
    
    if i % 100 == 0:
        print(f"Inserted {i} rows")

# Final commit
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully")
