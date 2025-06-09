from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import routes

app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)