#!/bin/sh

set -e

echo "Starting Ollama..."

# Start server in background
ollama serve &
OLLAMA_PID=$!

# Wait until API is ready
echo "Waiting for Ollama API..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

echo "Ollama is ready"

# Pull model
ollama pull nomic-embed-text

echo "Model ready"

# Keep container alive
wait $OLLAMA_PID