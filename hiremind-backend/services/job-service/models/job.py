from datetime import datetime
from typing import List

from beanie import Document
from pydantic import Field


class Job(Document):
    """MongoDB document model for a job posting."""

    title: str
    description: str
    skills: List[str]
    location: str
    experience_required: str
    deadline: datetime
    created_by: str         # user id of the HR who created the job
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "jobs"  # MongoDB collection name
