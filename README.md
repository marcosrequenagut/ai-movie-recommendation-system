# ai-movie-recommendation-system
"A recommendation system that scrapes articles and provides suggestions based on user reading history using LLM models.

ETL DE PREPROCESAMIENTO, DESCARGAR Y CARGA DE LOS DATOS:
add initial ETL pipeline for movie data ingestion and storage (CSV + PostgreSQL). Me he conectado a la API de donde he sacado los datos de las películas : cuyo endpoint es: # Endpoint for popular movies
    url = "https://api.themoviedb.org/3/movie/popular"
El otro endpoint usado para transformar una de las columans ha sido:
    url = "https://api.themoviedb.org/3/genre/movie/list"
Es para trasnformar los generos de las pelicuals de numeros a letras
He limpiado los datos, los he trasnformado convenientemente y los he subido a PostGreSQL y creado un csv local por si acaso. 