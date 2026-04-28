
def get_best_movie(results):

    """Function to get the best movie from the results and return its metadata"""

    # Introduce the explaination of the most recommended movie using a LLM called Ollama
    score_most_recommended_movie = 0
    for r in results:
        score = float(r[3])
        if score > score_most_recommended_movie:
            # Create a metadata using the most recommended movie
            dict_metadata = {
                "title": r[1],
                "genres": r[4],
                "overview": r[5],
                "release_year": r[6],
                "vote_average": r[7],
                "popularity": r[8],
            }

            score_most_recommended_movie = score

    return dict_metadata