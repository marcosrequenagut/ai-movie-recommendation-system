from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI()

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Movie Recommender API!"}
