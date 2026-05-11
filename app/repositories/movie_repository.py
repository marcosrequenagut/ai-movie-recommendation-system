

def search_movies_by_embedding(conn, embedding, allowed_ids, top_k):

    cur = conn.cursor()

    sql_query = """
        SELECT id, title, content,
               embedding <-> %s::vector AS distance,
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
        ORDER BY distance
        LIMIT %s
    """

    params.append(top_k)

    cur.execute(sql_query, params)
    results = cur.fetchall()

    cur.close()

    return results