
def get_best_movie(results):

    """Funtion that returns metada of the highest scoring movie."""

    if not results:
        return None
    
    best_score = float("-inf")
    best_movie = None

    for r in results:

        distance = float(r[3])
        score = distance # Is similarity not distance

        if score > best_score:
            # Create a metadata using the most recommended movies
            best_movie = {
                "id": r[0],
                "title": r[1],
                "genres": r[4],
                "overview": r[5],
                "release_year": r[6],
                "vote_average": r[7],
                "popularity": r[8],
            }

            best_score = score

    return best_movie

def get_weights(mode = "smart"):

    """
    Function to get the weights for the ranking of the movies based on the mode selected by the user.
    The mode can be "quality", "taste" or "smart".
    First value is the weight for the embedding score, second value is the weight for the genre
    matching and third value is the weight for the weighted rating.
    """

    weights = {
        "quality": (0.40, 0.15, 0.45),  # priorize rating
        "taste":   (0.60, 0.30, 0.10),  # priorize similitud + géneros
        "smart":   (0.65, 0.20, 0.15),  # priorize similitud semántica
    }
    
    # Return weights, default: smart
    return weights.get(mode, weights["smart"])


def rank_movies(candidates, user_filters=None, user_mode="smart"):
    """
    Rank movies using hybrid scoring (embedding + genre + rating)
    """

    user_filters = user_filters or {}
    user_genres = set(user_filters.get("genres", []))

    def score(x):
        # 1. embedding 
        embedding_score = float(x[3])  # Assuming x[3] it is not distance but the cosine similarity score from the DB.
        print(F"EMBEDDING SCORE: {embedding_score} - {x[1]}")

        # 2 genres matching
        movie_genres = set(x[4] or [])

        if user_genres:
            genre_score = len(user_genres & movie_genres) / len(user_genres)
        else:
            genre_score = 0.5 # neutral

        # 3. weighted rating. 
        weighted_rating = float(x[7])  # Assuming x[7] is the weighted rating from the DB, from 0 to 1

        # Weights for each component
        w_emb, w_genres, w_rating = get_weights(user_mode)

        final_score = w_emb * embedding_score + w_genres * genre_score + w_rating * weighted_rating
        print (f"FINAL SCORE: {final_score} - {x[1]} \n")

        # Final score is a weighted sum of the three components
        return final_score

    # x[3] is the cosine similarity calculated in the BD using SQL and reverse=False because fewer distance = better movie
    return sorted(candidates, key=score, reverse=True)