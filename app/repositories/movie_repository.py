

def search_movies_by_embedding(conn, embedding, allowed_ids, top_k):

    cur = conn.cursor()

    # 1 - (...) gives cosine similarity not cosine distance
    sql_query = """
        SELECT id, title, content,
               1 - (embedding <=> %s::vector) AS similarity,
               genres, overview, release_year, vote_average, popularity
        FROM movies
    """

    params = [embedding]

    if allowed_ids:
        if not isinstance(allowed_ids, list):
            allowed_ids = [allowed_ids]

        sql_query += " WHERE id = ANY(%s)"
        params.append(allowed_ids)

    sql_query += """
        ORDER BY similarity DESC
        LIMIT %s
    """

    params.append(top_k)

    cur.execute(sql_query, params)
    results = cur.fetchall()

    cur.close()

    return results

def search_movie_by_id(conn, movie_id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, overview, genres, release_year, vote_average, popularity
        FROM movies
        WHERE id = %s
    """, [movie_id])
    result = cur.fetchone()
    cur.close()
    return result