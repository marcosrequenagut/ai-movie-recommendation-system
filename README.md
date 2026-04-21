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