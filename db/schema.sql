-- Activar extensión para embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabla principal
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    embedding vector(1536)
);


CREATE INDEX IF NOT EXISTS movies_embedding_idx
ON movies
USING ivfflat (embedding vector_cosine_ops);