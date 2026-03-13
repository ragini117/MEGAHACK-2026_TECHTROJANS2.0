from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class Organization(Document):
    """
    MongoDB document model for an organization.

    Collection: organizations
    HR users reference this via organization_id.
    """

    name: str
    industry: str
    size: Optional[int] = None          # headcount
    location: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "organizations"
