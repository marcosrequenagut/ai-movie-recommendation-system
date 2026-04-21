from app.db.connection import get_connection
from app.embeddings.get_embeding import get_embedding

def get_recommended_movies(query, top_k=10):

    conn = get_connection()
    cur = conn.cursor()

    # query_embedding = str(get_embedding(query))
    query_embedding = get_embedding(query)

    # Implementation for fetching recommended movies based on embedding similarity
    sql_query = """
        SELECT id, title, content,
               embedding <-> %s AS cosine_distance
        FROM movies
        ORDER BY cosine_distance
        LIMIT %s;
    """
    
    cur.execute(sql_query, (query_embedding, top_k))

    results = cur.fetchall()

    cur.close()
    conn.close()
    
    return results

