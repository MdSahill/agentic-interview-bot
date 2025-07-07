from fastapi import FastAPI
from app.routers import interview, health

app = FastAPI(
    title="Agentic AI Interview Bot",
    version="0.1",
)

app.include_router(health.router)
app.include_router(interview.router)