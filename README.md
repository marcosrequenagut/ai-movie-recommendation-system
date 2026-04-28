# ai-movie-recommendation-system
"A recommendation system that scrapes articles and provides suggestions based on user reading history using LLM models.

ETL DE PREPROCESAMIENTO, DESCARGAR Y CARGA DE LOS DATOS:
add initial ETL pipeline for movie data ingestion and storage (CSV + PostgreSQL). Me he conectado a la API de donde he sacado los datos de las películas : cuyo endpoint es: # Endpoint for popular movies
    url = "https://api.themoviedb.org/3/movie/popular"
El otro endpoint usado para transformar una de las columans ha sido:
    url = "https://api.themoviedb.org/3/genre/movie/list"
Es para trasnformar los generos de las pelicuals de numeros a letras
He limpiado los datos, los he trasnformado convenientemente y los he subido a PostGreSQL y creado un csv local por si acaso. 

hay que descargar ollama y ollama pull nomic-embed-text para los embedings, se hace automaticamente por ollama

cómo trabajan juntos
Dockerfile → crea imagen de la API
docker-compose → levanta API + DB + red
API conecta a DB usando db:5432

[ FastAPI container ]  --->  [ PostgreSQL + pgvector container ]
         |                              |
      puerto 8000                  puerto 5432

Para levantar postgree para subir los datos tengoq que hacer:

docker run --name movie-postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=movies_db \
  -p 5432:5432 \
  -d pgvector/pgvector:pg15

Los datos se cogen de una api y se meten en postgree usando el codigo db/connecion.py. Para ello esos datos se han guardado en local como csv, se han leido otra vez y se han metido en postgree. Se podría hacer más directo, leyendo directamente de la api y guardadno en postgre directamente.

tipos de commit para tenerlo todo ordenado

feat(api): add recommendation endpoint
fix(db): fix vector type mismatch
refactor(recommender): improve query structure
chore(docker): add postgres service

CADA VEZ QUE SE REINICIE LA APP HABRÁ QUE HACER:


docker run --name movies_postgree \
  -e POSTGRES_DB=movies_db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -p 5432:5432 \
  -v ${PWD}/app/db/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -d pgvector/pgvector:pg15

# 3. Esperar unos segundos a que PostgreSQL inicie
sleep 5

# 4. Habilitar la extensión (opcional, ya viene preinstalada)
docker exec -it movies_postgree psql -U admin -d movies_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

# 5. Verificar que funciona
docker exec -it movies_postgree psql -U admin -d movies_db -c "SELECT * FROM pg_extension WHERE extname='vector';"

Primera vez que inicio el contendor:

docker compose build --no-cache
docker compose up 
python -m app.scripts.fill_postgree_db

# Lo unico que me funcion para ejecutar python es esto:  python -m app.scripts.fill_postgree_db

# Modelos a descargar para que funcione la app:
docker exec -it ollama ollama pull tinyllama
docker exec -it ollama ollama pull mistral (este tarda como 10 minutos porque es muy grande)
docker exec -it ollama ollama pull nomic-embed-text:latest
docker exec -it ollama ollama list para comprobar si ambos modelos se han descarrfo bien































PROJECT STATUS PROMPT — Movie Recommender System

You are working on a modular AI movie recommendation system with an agent-based architecture.

📌 CURRENT ARCHITECTURE
1. Agent (dispatcher layer)
Receives: user_input
Calls: decide_action(user_input)
Routes request to a tool based on action
Executes tools from a registry

Current behavior:

"recommend" → recommendation pipeline
"explain" → explanation tool

Status: ✔ working
Weakness: still depends on fragile LLM JSON output

2. Router (decide_action)
Uses LLM (Ollama / Mistral)
Outputs structured JSON:
{
  "action": "recommend | explain | clarify",
  "query": "...",
  "movie": "..."
}

Status:
✔ functional
❌ fragile (can fail due to invalid JSON, missing keys, hallucinated fields)

👉 THIS IS THE MAIN SYSTEM WEAK POINT

3. Tool Registry

Maps actions → functions:

TOOLS = {
    "recommend": recommend_pipeline,
    "explain": generate_explanation
}

Status: ✔ correct and extensible

4. Recommendation Pipeline

Pipeline stages:

embed_query(query)
retrieve_movies (pgvector search in Postgres)
apply optional filtering (allowed_ids from SQL filter)
rank_movies
return top-K results

Status: ✔ fully working

5. Filter System
Uses FilterRequest
SQL filtering returns allowed_ids
integrated into pipeline

Status: ✔ working after fixes

6. Explain Tool
Calls LLM (Ollama)
Generates natural language explanation of a movie

Status: ✔ working but depends on external Ollama service

7. Database Layer
PostgreSQL + pgvector
embedding similarity search using <->
retrieval returns ranked candidates

Status: ✔ stable after fixing SQL parameter issues

🚨 CURRENT SYSTEM STATE

✔ End-to-end pipeline works
✔ Agent → Tools → Pipeline flow is functional
✔ Retrieval + ranking + filtering are correct
✔ Architecture is already LangGraph-ready conceptually

❌ Main weakness:

decide_action is fragile and LLM-dependent
JSON parsing can fail
schema not enforced
🎯 NEXT STEPS (IMPORTANT ROADMAP)
STEP 1 — Fix router robustness (HIGHEST PRIORITY)

Replace fragile LLM JSON with:

structured output parsing
validation layer (Pydantic or schema enforcement)
fallback parsing if JSON fails

Goal:
👉 make decide_action deterministic and safe

STEP 2 — Standardize tool input format

Move toward:

tool(input: dict)

Where all tools accept a unified structure:

query
filters
top_k
movie
metadata

Goal:
👉 remove dependency on agent knowing tool signatures

STEP 3 — Simplify agent into pure dispatcher

Agent should become:

decision = decide_action(input)
return TOOLS[decision["action"]](decision)

Goal:
👉 zero business logic in agent

STEP 4 — Prepare LangGraph migration

Once stable:

each tool = node
agent = router node
state = shared dict

Goal:
👉 easy migration to graph-based execution

🧭 FINAL STATE YOU ARE AIMING FOR

A system where:

routing is robust (no fragile JSON failures)
tools are stateless and standardized
agent is a pure dispatcher
pipeline is composable
ready for LangGraph orchestration