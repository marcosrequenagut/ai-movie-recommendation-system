# AI Movie Recommendation System

An AI-powered movie recommendation system built with:

- FastAPI
- PostgreSQL + pgvector
- Ollama
- LangGraph
- Streamlit

The system combines semantic search, vector embeddings, LLM-based routing, hybrid ranking, conversational memory, and AI-generated explanations to provide intelligent movie recommendations.

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
- [Conversational Memory](#conversational-memory)
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

## Conversational Memory

The system maintains persistent conversational memory across API calls using LangGraph's checkpointer with SQLite. Each conversation is identified by a `thread_id`, allowing users to refine recommendations across multiple turns.

- State is persisted to disk between calls using `SqliteSaver`
- Each conversation is identified by a `thread_id`
- The conversation history accumulates user queries and assistant responses
- The router uses the full conversation history to understand follow-up requests

### Example

```text
Call 1: "Recommend emotional sci-fi movies"
→ ["Her", "Arrival", "WALL·E", "Finch", "Interstellar"]

Call 2 (same thread_id): "add horror and remove sci-fi"
→ Router understands the context and adjusts filters accordingly
→ ["Get Out", "Hereditary", "A Desert", "Se7en", "Scream"]
```

---

## Query Contextualization

Before processing, a dedicated node rewrites the user's current query into a single enriched query that captures the full intent of the conversation so far.

- Reads all previous user queries from the conversation history
- Uses the LLM to merge and resolve contradictions between past and current preferences
- Produces one final query optimized for semantic search and embeddings
- The raw original query is preserved separately and stored in the history to avoid contextual drift

### Example

```text
QUERY 1: "Recommend emotional sci-fi movies"
QUERY 2: "I want something scarier"
QUERY 3: "Actually make it realistic, not sci-fi"

→ Contextualized query: "realistic emotional thriller and drama movies without sci-fi elements"
```

---

## Hybrid Ranking System

Movies are ranked using:

- Embedding similarity (converted from distance to similarity via `1 / (1 + distance)`)
- Genre matching
- Weighted movie rating (normalized to 0–1)

The user can choose recommendation modes:

| Mode | Description |
|---|---|
| `smart` | Prioritizes semantic similarity (weights: 0.65 / 0.20 / 0.15) |
| `quality` | Prioritizes highly rated movies (weights: 0.40 / 0.15 / 0.45) |
| `taste` | Prioritizes genre similarity (weights: 0.60 / 0.30 / 0.10) |

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
contextualize_query       ← rewrites query using full conversation history
  ↓
semantic_filter           ← extracts active genres from context + current query
  ↓
router                    ← classifies intent using query + conversation history
  ↓
query_expansion           ← generates 3 semantic variants (only for recommend)
  ↓
recommend / explain / clarify
  ↓
format_output_node        ← updates conversation history
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

The router receives the full conversation history as context, allowing it to correctly classify follow-up requests like "add horror" or "only from the 90s" as `recommend` actions rather than ambiguous queries.

---

## Semantic Genre Filter

A dedicated node uses the LLM to determine which genres should be active based on the full conversation context and the current user request.

- Reads only user messages from the conversation history to understand genre evolution
- Handles additions ("add horror") and removals ("remove sci-fi") intelligently
- Validates all detected genres against the official list to prevent hallucinations
- Detects synonyms and variants (e.g. "sci-fi" → "Science Fiction", "scary" → "Horror")

### Example

```text
History:  "Recommend emotional sci-fi movies"
Current:  "remove sci-fi and add horror"
→ active genres: ["Drama", "Horror"]  ← Science Fiction correctly removed
```

---

## Query Expansion

Before performing the vector search, a dedicated node uses the LLM to rewrite the contextualized query into 3 semantic variants. Each variant generates its own embedding, resulting in multiple vector searches whose results are merged and deduplicated.

- Improves recall for vague or short queries
- The contextualized query is always included alongside the expanded variants
- Deduplication keeps the result with the lowest distance (highest similarity) per movie
- Only executes when `action == "recommend"`

### Example

```text
"emotional sci-fi movies"
→ "philosophical science fiction with human drama"
→ "thought-provoking futuristic films about humanity"
→ "existential space stories with deep emotional themes"
→ 4 vector searches → merged unique candidates → ranking → top-K results
```

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
│   Agent +        │             │    Pipeline      │
│   SQLite Memory  │             └──────────────────┘
└──────────────────┘                       │
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
- SQLite (conversational memory)

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
│   └── data/
│       ├── memory/     # SQLite conversational memory (memory.db)
│       └── graph.png   # LangGraph visualization
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
| `mistral` | Router + query contextualization + genre extraction + query expansion |
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

Main AI recommendation endpoint. Supports conversational memory via `thread_id`.

## Request Example

```json
{
  "query": "Recommend emotional sci-fi movies",
  "top_k": 5,
  "filters": {
    "genres": ["Science Fiction"],
    "min_rating": 7.0,
    "year_from": 1990,
    "year_to": 2024
  },
  "user_mode": "smart",
  "thread_id": "my-conversation-1"
}
```

If no `thread_id` is provided, the system generates one automatically and returns it in the response. Use the same `thread_id` in subsequent calls to maintain conversational context.

## Response Example

```json
{
  "query": "Recommend emotional sci-fi movies",
  "action": "recommend",
  "movies": [
    "Her",
    "Interstellar",
    "Arrival",
    "WALL·E",
    "Blade Runner 2049"
  ],
  "thread_id": "my-conversation-1",
  "conversation_history": [
    {"role": "user", "content": "Recommend emotional sci-fi movies"},
    {"role": "assistant", "content": "I recommended the following movies: Her, Interstellar, Arrival, WALL·E, Blade Runner 2049"}
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
User Query (raw_query)
    ↓
Query Contextualization (LLM merges conversation history into one enriched query)
    ↓
Semantic Genre Filter (LLM determines active genres from context + current query)
    ↓
Router (classifies intent using contextualized query + conversation history)
    ↓
Query Expansion (LLM generates 3 semantic variants — only for recommend)
    ↓
Embedding Generation (one embedding per query variant)
    ↓
Multi Vector Search (one search per embedding, results merged and deduplicated)
    ↓
Filtering (by genre, rating, year)
    ↓
Hybrid Ranking
    ↓
Top-K Final Recommendations
    ↓
format_output_node (appends interaction to conversation_history)
```

---

# Conversational Memory

The system uses LangGraph's `SqliteSaver` checkpointer to persist the conversation state between API calls.

## How it works

Each call to `/agent` with a `thread_id` saves the full agent state to a local SQLite database. On the next call with the same `thread_id`, LangGraph automatically recovers the previous state including the `conversation_history`.

## thread_id

The `thread_id` is the identifier of a conversation. The client is responsible for sending the same `thread_id` across multiple calls to maintain context.

```text
Call 1: thread_id="abc" → no prior state → starts fresh → saves state
Call 2: thread_id="abc" → recovers state → uses conversation history → saves updated state
Call 3: thread_id="abc" → recovers state → continues conversation
```

## conversation_history

The history accumulates raw user queries and assistant responses. Raw queries are stored instead of contextualized ones to avoid contextual drift across multiple turns.

```json
[
  {"role": "user", "content": "Recommend emotional sci-fi movies"},
  {"role": "assistant", "content": "I recommended the following movies: Her, Arrival, WALL·E"},
  {"role": "user", "content": "add horror and remove sci-fi"},
  {"role": "assistant", "content": "I recommended the following movies: Get Out, Hereditary, Se7en"}
]
```

## SQLite Location

```text
data_processing/data/memory/memory.db
```

---

# Ranking System

The final score combines three normalized components (all in 0–1 range):

- **Embedding similarity**: converted from pgvector distance using `1 / (1 + distance)`
- **Genre matching**: ratio of matched genres over requested genres
- **Weighted rating**: vote average normalized to 0–1

### Formula

```text
Final Score =
    w_embedding  * embedding_similarity
  + w_genre      * genre_match_score
  + w_rating     * normalized_rating
```

The weights change depending on the selected recommendation mode:

| Mode | Embedding | Genre | Rating |
|---|---|---|---|
| `smart` | 0.65 | 0.20 | 0.15 |
| `quality` | 0.40 | 0.15 | 0.45 |
| `taste` | 0.60 | 0.30 | 0.10 |

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

- User profiles
- RAG over movie reviews
- Movie similarity search ("something like Interstellar")
- Async FastAPI endpoints
- Redis caching for conversation state
- GPU inference
- Evaluation metrics
- Multi-agent workflows
- Recommendation feedback loops
- Frontend conversational UI in Streamlit

---

# License

MIT License

---

# Author

Juan Marcos Requena Gutiérrez
