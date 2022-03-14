# Imports
from fastapi import FastAPI
import models
from database_connection import engine
from routers import items
from fastapi.middleware.cors import CORSMiddleware

# Creating all models
models.Base.metadata.create_all(bind=engine)

# Instance of FastAPI
app = FastAPI()

# Allowed "origins" list
origins = [
    "http://localhost",
    "http://localhost:8080",
]

# "CORS" policy parameters
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Grabbing "router" object from item.py
app.include_router(items.router)

@app.get("/")
async def root():
	return {"message":"Welcome to TODO List FastAPI"}