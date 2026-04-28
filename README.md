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































Estoy desarrollando un proyecto personal cuyo objetivo es aprender y experimentar con tecnologías relacionadas con sistemas de recomendación y agentes de IA. Quiero que actúes como un arquitecto de software senior especializado en IA y me ayudes a escalar el proyecto, mejorar su diseño y proponer nuevas funcionalidades y tecnologías (especialmente LangChain y LangGraph).

### 🎯 Objetivo del proyecto

Construir un sistema de recomendación de películas basado en embeddings y evolucionarlo hacia un sistema más avanzado con agentes de IA capaces de razonar, tomar decisiones y orquestar tareas.

---

### ⚙️ Estado actual del proyecto

#### Flujo de datos:

1. Me conecto a una API de películas.
2. Descargo los datos en un CSV.
3. Para cada película genero un embedding combinando:

   * Géneros
   * Overview (descripción)
   * Título
4. Almaceno estos embeddings para luego hacer búsquedas semánticas.

---

### 🚀 Backend (FastAPI)

Tengo varios endpoints tipo POST:

* **recommender.py**
  Recomienda películas en base a un prompt del usuario
  Ejemplo: *"recomiéndame una peli de drama que tenga que ver con el infierno"*

* **filter.py**
  Permite filtrar por atributos como género, año, etc.

* **explainer.py**
  Usa un modelo para explicar por qué se ha recomendado una película

* **agent.py**
  Implementa un agente simple que:

  * Decide si usar recommender o explainer según el prompt
  * Si no entiende el prompt, pide reformulación

---

### 🗂️ Estructura del proyecto

app/
├── agent/
├── api/
│   └── routes/
├── db/
├── embeddings/
├── recommender/
├── repositories/
├── scripts/
├── service/

data_processing/
└── data/

infra/
└── ollama/

---

### 🐳 Infraestructura

Todo está dockerizado:

* Contenedor de modelos con Ollama
* Contenedor de PostgreSQL
* Contenedor de FastAPI

---

### 🎯 Objetivo actual

Quiero escalar el proyecto y convertirlo en algo más avanzado. Mis intereses principales son:

* Aprender e integrar **LangChain**
* Aprender e integrar **LangGraph**
* Diseñar agentes más complejos y útiles
* Mejorar la arquitectura del sistema
* Añadir nuevas capacidades (memoria, razonamiento, multi-step workflows, etc.)

⚠️ Streamlit lo dejaré para el final (primero quiero tener un backend sólido).

---

### ❓ Lo que necesito de ti

1. Analiza mi arquitectura actual y dime:

   * Qué está bien
   * Qué debería mejorar

2. Propón una evolución del sistema:

   * Cómo introducir LangChain o LangGraph
   * Qué tipo de agentes podría construir
   * Cómo rediseñar el agente actual

3. Sugiere nuevas funcionalidades interesantes, por ejemplo:

   * Sistemas multi-agente
   * Memoria conversacional
   * RAG (Retrieval Augmented Generation)
   * Evaluación de recomendaciones

4. Propón un roadmap claro de aprendizaje e implementación (por fases)

5. Si detectas malas prácticas o limitaciones, dímelo claramente

---

Quiero una respuesta técnica, estructurada y orientada a llevar este proyecto a un nivel profesional.
