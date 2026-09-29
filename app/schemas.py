from typing import Any
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: str
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10000000)
    rooms: list[str] = Field(min_length=1)
    style: str = Field(default="Modern", max_length=100)
    notes: str = Field(default="", max_length=1000)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10000000)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = Field(default="", max_length=200)
    notes: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10000000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="Elegant", max_length=100)
    notes: str = Field(default="", max_length=1000)
