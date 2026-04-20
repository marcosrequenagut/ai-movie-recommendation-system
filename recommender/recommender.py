from db.connection import get_connection
from embeddings.get_embeding import get_embedding

cur = get_connection().cursor()

def get_recommended_movies(query, top_k=10):

    query_embedding = str(get_embedding(query))

    # Implementation for fetching recommended movies based on embedding similarity
    sql_query = """
        SELECT id, title, content,
               embedding <-> %s AS cosine_distance
        FROM movies
        ORDER BY cosine_distance
        LIMIT %s;
    """
    
    cur.execute(sql_query, (query_embedding, top_k))

    return cur.fetchall()

