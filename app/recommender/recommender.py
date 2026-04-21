from app.db.connection import get_connection
from app.embeddings.get_embeding import get_embedding

def get_recommended_movies(query, top_k=10, allowed_ids=None):

    conn = get_connection()
    cur = conn.cursor()

    query_embedding = get_embedding(query)

    # Implementation for fetching recommended movies based on embedding similarity
    sql_query = """
        SELECT id, title, content,
               embedding <-> %s::vector AS cosine_distance,
                genres
        FROM movies
    """

    params = [query_embedding]

    if allowed_ids:
        sql_query += " WHERE id = ANY(%s)"
        params.append(allowed_ids)

    sql_query += """
        ORDER BY cosine_distance
        LIMIT %s
    """

    params.append(top_k)

    cur.execute(sql_query, params)

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results

