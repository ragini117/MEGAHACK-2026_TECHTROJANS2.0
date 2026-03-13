from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator


class JobCreateSchema(BaseModel):
    title: str
    description: str
    skills: List[str]
    location: str
    experience_required: str
    deadline: datetime

    @field_validator("title", "description", "location", "experience_required")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()

    @field_validator("skills")
    @classmethod
    def skills_not_empty(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one skill is required")
        return v


class JobResponseSchema(BaseModel):
    id: str
    title: str
    description: str
    skills: List[str]
    location: str
    experience_required: str
    deadline: str
    created_by: str
    created_at: str
