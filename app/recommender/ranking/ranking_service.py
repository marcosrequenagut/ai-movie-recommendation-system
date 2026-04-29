
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

def get_weights(mode = "smart"):

    """
    Function to get the weights for the ranking of the movies based on the mode selected by the user.
    The mode can be "quality", "taste" or "smart".
    First value is the weight for the embedding score, second value is the weight for the genre
    matching and third value is the weight for the weighted rating.
    """

    if mode == "quality":
        return 0.45, 0.20, 0.35
    
    if mode == "taste":
        return 0.50, 0.35, 0.15
    
    # default: smart
    return 0.55, 0.25, 0.20


def rank_movies(candidates, user_filters=None):
    """
    Basic Ranking in python (phase 1)
    Now, it respects the score of the DB.
    In the future, we will abstract it to upgrade it."""

    user_filters = user_filters or {}
    user_genres = set(user_filters.get("genres", []))
    user_mode = user_filters.get("user_mode", "smart")



    def score(x, user_mode=user_mode):
        # 1. embedding
        embedding_score = float(x[3])  # Assuming x[3] is the cosine similarity score from the DB
        print("EMBEDDING SCORE:", embedding_score)

        # 2 genres matching
        movie_genres = set(x[4] or [])
        if user_genres:
            genre_score = len(user_genres & movie_genres) / len(user_genres)
        else:
            genre_score = 0.5 # neutral

        # 3. weighted rating. 
        weighted_rating = float(x[7])  # Assuming x[7] is the weighted rating from the D

        # Weights for each component
        w_emb, w_genres, w_rating = get_weights(user_mode)

        # Final score is a weighted sum of the three components
        final_score = (
            w_emb * embedding_score +
            w_genres * genre_score +
            w_rating * weighted_rating
        )

    # x[3] is the cosine similarity calculated in the BD using SQL and reverse=False because fewer distance = better movie
    return sorted(candidates, key=score, reverse=True)