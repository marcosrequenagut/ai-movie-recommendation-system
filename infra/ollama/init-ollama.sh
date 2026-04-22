#!/bin/sh

# Start the Ollama server in the background
ollama serve &

# Wait a few seconds to allow the server to start
sleep 3

# Pull the embedding model if it is not already available
ollama pull nomic-embed-text

# Keep the container running and wait for background processes
wait