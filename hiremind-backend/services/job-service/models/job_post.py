from datetime import datetime
from typing import List, Optional

from beanie import Document
from pydantic import Field


class JobPost(Document):
    """
    MongoDB document model for a job post.

    Collection: job_posts
    """

    title: str
    description: str
    skills: List[str]
    experience: str                        # e.g. "2-4 years", "Fresher"
    location: str
    ctc: str                               # Cost-to-Company, e.g. "8-12 LPA"
    start_time: datetime                   # Job opening / application start date-time
    end_time: datetime                     # Application deadline / closing date-time
    created_by: str                        # user _id of the HR who posted this job
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "job_posts"                 # MongoDB collection name
