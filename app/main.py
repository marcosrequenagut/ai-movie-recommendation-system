from fastapi import FastAPI

from app.api.routes import router as api_router
from app.service.routes import router as filter_router

app = FastAPI()

app.include_router(api_router)
app.include_router(filter_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Movie Recommender API!"}
