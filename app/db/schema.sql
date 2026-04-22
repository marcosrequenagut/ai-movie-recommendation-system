-- Activate the exention for embeddings
CREATE EXTENSION IF NOT EXISTS vector;


-- Delete the table if it already EXISTS to create a new one
DROP TABLE IF EXISTS movies;

-- Main table
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    adult BOOLEAN,
    original_language TEXT,
    popularity FLOAT, 
    release_date TEXT,
    vote_average FLOAT,
    genres TEXT[],
    weighted_rating FLOAT,
    release_year INT,
    embedding vector(768),
    overview TEXT
);


CREATE INDEX IF NOT EXISTS movies_embedding_idx
ON movies
USING ivfflat (embedding vector_cosine_ops);