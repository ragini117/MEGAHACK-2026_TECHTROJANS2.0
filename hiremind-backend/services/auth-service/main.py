import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import connect_db, close_db
from routes.auth import router as auth_router
from routes.organization import router as org_router
from shared.middleware import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Auth Service",
    description="Authentication and Authorization microservice — AI Recruitment Platform",
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

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(org_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "auth-service", "version": "1.0.0"}
