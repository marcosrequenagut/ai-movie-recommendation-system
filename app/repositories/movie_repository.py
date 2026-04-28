

def search_movies_by_embedding(conn, embedding, allowed_ids, top_k):

    cur = conn.cursor()

    print("ALLOWED IDS EN MOVIE_REPOSITORY.PY:", allowed_ids, "TOP K:", top_k)

    sql_query = """
        SELECT id, title, content,
               embedding <-> %s::vector AS distance,
               genres, overview, release_year, vote_average, popularity
        FROM movies
    """

    params = [embedding]
    print("ALLOWED IDS:", allowed_ids)
    print("TOP K:", top_k)

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

    print("PARAMS:", params)
    print("NUM PARAMS:", len(params))
    print("NUM %s:", sql_query.count("%s"))
    print("SQL FINAL:")
    print(sql_query)

    cur.execute(sql_query, params)
    results = cur.fetchall()

    cur.close()

    return results