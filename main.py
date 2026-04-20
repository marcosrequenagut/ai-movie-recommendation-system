from recommender.recommender import get_recommended_movies

query = "A movie about a young wizard who discovers his magical heritage and attends a school of witchcraft and wizardry."

results = get_recommended_movies(query, top_k=10)

i = 1
for result in results:
    print(f"\n {i} Movie: ", result[1])
    i += 1