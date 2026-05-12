# AI Movie Recommendation System

An AI-powered movie recommendation system built with:

- FastAPI
- PostgreSQL + pgvector
- Ollama
- LangGraph
- Streamlit

The system combines semantic search, vector embeddings, LLM-based routing, hybrid ranking, and AI-generated explanations to provide intelligent movie recommendations.

---

# Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Dataset and ETL](#dataset-and-etl)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Ollama Models](#ollama-models)
- [Database Initialization](#database-initialization)
- [Running the System](#running-the-system)
- [API Endpoints](#api-endpoints)
- [Recommendation Pipeline](#recommendation-pipeline)
- [Ranking System](#ranking-system)
- [Docker Services](#docker-services)
- [Environment Variables](#environment-variables)
- [Future Improvements](#future-improvements)

---

# Features

## Semantic Movie Recommendations

The system converts user queries into embeddings using:

- `nomic-embed-text`

Then retrieves semantically similar movies from PostgreSQL using pgvector.

### Example

```text
"Recommend emotional sci-fi movies with philosophical themes"
```

---

## Hybrid Ranking System

Movies are ranked using:

- Embedding similarity
- Genre matching
- Weighted movie rating

The user can choose recommendation modes:

| Mode | Description |
|---|---|
| `smart` | Balanced recommendations |
| `quality` | Prioritize highly rated movies |
| `taste` | Prioritize genre similarity |

---

## LangGraph AI Agent

The recommendation workflow is orchestrated using LangGraph.

The AI agent can:

- Recommend movies
- Explain recommendations
- Ask clarification questions

### LangGraph Workflow

```text
START
  ↓
router
  ↓
recommend / explain / clarify
  ↓
format_output_node
  ↓
END
```

---

## LLM-Based Routing

The router uses:

- `mistral`

to classify user intent into:

- `recommend`
- `explain`
- `clarify`

---

## Recommendation Explanations

The system uses:

- `tinyllama`

to generate natural language explanations about why a movie was recommended.

---

# Architecture

```text
                ┌────────────────────┐
                │     Streamlit UI   │
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │      FastAPI       │
                └──────────┬─────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
┌──────────────────┐             ┌──────────────────┐
│   LangGraph AI   │             │ Recommendation   │
│      Agent       │             │    Pipeline      │
└──────────────────┘             └──────────────────┘
                                           │
                                           ▼
                                ┌──────────────────┐
                                │ PostgreSQL +     │
                                │    pgvector      │
                                └──────────────────┘
                                           │
                                           ▼
                                ┌──────────────────┐
                                │      Ollama      │
                                │ Embeddings + LLM │
                                └──────────────────┘
```

---

# Tech Stack

## Backend

- FastAPI
- LangGraph
- PostgreSQL
- pgvector
- Pydantic

## AI / Machine Learning

- Ollama
- nomic-embed-text
- mistral
- tinyllama

## Frontend

- Streamlit

## Infrastructure

- Docker
- Docker Compose

---

# Project Structure

```text
app/
│
├── agent/              # LangGraph agent system
├── api/                # FastAPI routes
├── db/                 # PostgreSQL connection + SQL schema
├── embeddings/         # Embedding generation
├── recommender/        # Recommendation logic
├── repositories/       # Database queries
├── retrieval/          # Vector retrieval layer
├── service/            # Business logic
├── scripts/            # Database population scripts
├── ui/                 # Streamlit frontend
│
data_processing/
│
infra/
```

---

# Dataset and ETL

Movie data is obtained from TMDB API.

### Endpoints Used

```text
/movie/popular
/genre/movie/list
```

### ETL Process

1. Download movie metadata
2. Clean and preprocess the data
3. Transform genre IDs into readable labels
4. Generate embeddings
5. Store data in PostgreSQL
6. Save local CSV backups

---

# Installation

## Clone Repository

```bash
git clone https://github.com/marcosrequenagut/ai-movie-recommendation-system

cd ai-movie-recommendation-system
```

---

# Requirements

- Docker
- Docker Compose
- Python 3.9+
- Ollama

---

# Docker Setup

## Build Containers

```bash
docker compose build --no-cache
```

## Start Containers

```bash
docker compose up
```

---

# PostgreSQL + pgvector Setup

## Create PostgreSQL Container

```bash
docker run --name movies_postgree \
  -e POSTGRES_DB=movies_db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -p 5432:5432 \
  -v ${PWD}/app/db/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -d pgvector/pgvector:pg15
```

---

# Database Initialization

## Enable pgvector Extension

```bash
docker exec -it movies_postgree psql -U admin -d movies_db \
-c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Verify Installation

```bash
docker exec -it movies_postgree psql -U admin -d movies_db \
-c "SELECT * FROM pg_extension WHERE extname='vector';"
```

---

# Ollama Models

The system requires the following models:

| Model | Purpose |
|---|---|
| `mistral` | Router decision |
| `tinyllama` | Recommendation explanation |
| `nomic-embed-text` | Embedding generation |

---

## Download Models

### tinyllama

```bash
docker exec -it ollama ollama pull tinyllama
```

### mistral

```bash
docker exec -it ollama ollama pull mistral
```

### nomic-embed-text

```bash
docker exec -it ollama ollama pull nomic-embed-text:latest
```

### Verify Models

```bash
docker exec -it ollama ollama list
```

---

# Populate PostgreSQL Database

Run:

```bash
python -m app.scripts.fill_postgree_db
```

---

# Running the System

## FastAPI

The API will be available at:

```text
http://localhost:8000
```

### Swagger Documentation

```text
http://localhost:8000/docs
```

---

## Streamlit Frontend

The UI will be available at:

```text
http://localhost:8501
```

---

# API Endpoints

# POST `/agent`

Main AI recommendation endpoint.

## Request Example

```json
{
  "query": "Recommend emotional sci-fi movies",
  "top_k": 5,
  "filters": {
    "genres": ["Science Fiction"],
    "min_rating": 7.0
  },
  "user_mode": "smart"
}
```

## Response Example

```json
{
  "query": "Recommend emotional sci-fi movies",
  "action": "recommend",
  "movies": [
    "Interstellar",
    "Arrival",
    "Blade Runner 2049"
  ]
}
```

---

# POST `/filter`

Apply direct movie filters.

## Request Example

```json
{
  "genres": ["Action"],
  "min_rating": 7.5,
  "year_from": 2000,
  "year_to": 2024
}
```

---

# POST `/explain`

Generate explanation for a recommendation.

---

# Recommendation Pipeline

```text
User Query
    ↓
Embedding Generation
    ↓
Vector Search (pgvector)
    ↓
Filtering
    ↓
Hybrid Ranking
    ↓
Final Recommendations
```

---

# Ranking System

The final score combines:

- Embedding similarity
- Genre matching
- Weighted movie rating

### Formula

```text
Final Score =
    Embedding Similarity
  + Genre Matching
  + Weighted Rating
```

The weights change depending on the selected recommendation mode.

---

# Docker Services

| Service | Port |
|---|---|
| FastAPI | 8000 |
| PostgreSQL | 5432 |
| Ollama | 11434 |
| Streamlit | 8501 |

---

# Environment Variables

```env
DB_HOST=db
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=admin
DB_NAME=movies_db
```

---

# Common Docker Commands

## Rebuild Containers

```bash
docker compose build --no-cache
```

## Restart System

```bash
docker compose down

docker compose up
```

## View Logs

### FastAPI Logs

```bash
docker logs movie-api
```

### Ollama Logs

```bash
docker logs ollama
```

### PostgreSQL Logs

```bash
docker logs movies_postgree
```

# COSAS NUEVAS AÑADIDAS QUE HAY QUE METER EN LA SIGUIENTE VERSION DEL README.MD
1.- HE CREADO UN NUEVO NODO QUE SE EJECUTA SOLO UNA VEZ. LO QUE HACE ES DETECTAR USANDO UN LLM SI EN LA QUERY DEL USUARIO HAY GENEROS DE PELICULAS ESCONDIDOS PARA AÑADIRLOS AL FILTRO. ESOS GENEROS SE HAÑADEN Y NO SE REPITEN NI NADA.

2.- SOLO SE EJECUTA 1 VEZ ESTE NODO, SE ACTIVA MEDIANTE UN FLAG EN ELE STADO. TRAS EL ROUTER SIEMRPE SE EJECUTA Y ENTONCES EL FLAG PASA A SER TRUE. SE HA HECHO ESTO PORQUE EL NODO CLARIFY SI SALE COMO ACTION=CLARIFY VUELVE AL ROUTER Y TRAS EL ROUTER VA EL SEMANTINC_FILTER ENTONCES PARA QUE NO SE EJECUTE 10 VECES EL MISMO FILTRO, SE SALTA TRAS HABERSE EJECUTADO LA 1 VZ

3.- CREACIÓN DE UN NUEVO NODO:
def query_expansion_node(state: AgentState) -> Dict[str: Any]:
    """
    This function expands the user query into 3 semantic variants using the LLM.
    This improve vector search recall by covering more semantic ground.
    Only runs when action == "recommmend
    """
---

# Commit Convention

```text
feat(api): add recommendation endpoint
fix(db): fix vector type mismatch
refactor(recommender): improve query structure
chore(docker): add postgres service
```

---

# Future Improvements

- Conversational memory
- User profiles
- RAG over movie reviews
- Better reranking strategies
- Async FastAPI endpoints
- Redis caching
- GPU inference
- Evaluation metrics
- Multi-agent workflows
- Recommendation feedback loops

---

# License

MIT License

---

# Author

Juan Marcos Requena Gutiérrez