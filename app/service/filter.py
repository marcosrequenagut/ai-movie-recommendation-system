from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.db.connection import get_connection

app = APIRouter()

class FilterRequest(BaseModel):
    genres: list[str] = Field(default_factory=list)
    min_rating: float = 0.0
    year_from: int = 1900
    year_to: int = 2100

    
