"""
Shared configuration reference.
Each microservice reads its own .env file.
Copy relevant variables into each service's .env as needed.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_recruitment")

# JWT
JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret-in-production")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# Service base URLs
AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
JOB_SERVICE_URL: str = os.getenv("JOB_SERVICE_URL", "http://localhost:8002")
DISTRIBUTION_SERVICE_URL: str = os.getenv("DISTRIBUTION_SERVICE_URL", "http://localhost:8003")
APPLICATION_SERVICE_URL: str = os.getenv("APPLICATION_SERVICE_URL", "http://localhost:8004")
