import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import connect_db, close_db
from routes.jobs import router as jobs_router
from routes.job_post import router as job_post_router
from shared.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Job Service",
    description="Job creation and management microservice — AI Recruitment Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)

app.include_router(jobs_router, tags=["Jobs"])
app.include_router(job_post_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "job-service", "version": "1.0.0"}
