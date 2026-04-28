'''from app.service.recommendation_pipeline import recommend_pipeline

# TEST 1

results = recommend_pipeline(
    query="a dark sci-fi movie about space",
    filters=None,
    top_k=5
)
'''
#print(results)

'''# TEST 2

from app.recommender.ranking.ranking_service import rank_movies
result = rank_movies([
    (1, "A", "x", 0.9),
    (2, "B", "x", 0.1),
    (3, "C", "x", 0.5),
])

#print("\n\n\nRanking movies:", result)

# TEST 3
# ✔ debe devolver candidatos (más de top_k si SQL lo permite o exactamente top_k)
from app.retrieval.retrieval_service import retrieve_movies
from app.embeddings.service import embed_query

embedding = embed_query("space sci-fi")

results = retrieve_movies(
    query_embedding=embedding,
    allowed_ids=None,
    top_k=10
)'''

#print(len(results))

# 4. TEST DEL AGENTE (CRÍTICO)
# Debe devolver lista de películas
'''from app.agent.agent import agent

print("\n\n\n\n\n\n\n\nTEST DEL AGENTE:\n\n\n\n\n\n\n\n")

result = agent(
    user_input="recommend me a dark sci-fi movie",
    filters=None,
    top_k=5
)

print(result)'''

#5. TEST DE EXPLAINER
# debe devolver texto natural
from app.service.explainer import generate_explanation
print("\n\n\n\n\n\n\n\nTEST DEL EXPLAINER:\n\n\n\n\n\n\n\n")
print(
    generate_explanation(
        query="dark sci-fi movie",
        movie="Interstellar",
        metadata={"genre": "sci-fi"}
    )
)
