
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

def rank_movies(candidates):
    """
    Basic Ranking in python (phase 1)
    Now, it respects the score of the DB.
    In the future, we will abstract it to upgrade it."""

    # x[3] is the cosine similarity calculated in the BD using SQL and reverse=False because fewer distance = better movie
    return sorted(candidates, key= lambda x: float(x[3]), revserse=False)