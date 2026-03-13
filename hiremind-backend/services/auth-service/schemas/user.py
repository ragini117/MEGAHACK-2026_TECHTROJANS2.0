from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class OrganizationInlineSchema(BaseModel):
    """Organization details filled inline during HR registration."""
    name: str
    industry: str
    size: Optional[int] = None
    location: str

    @field_validator("name", "industry", "location")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class UserRole(str, Enum):
    hr = "hr"
    candidate = "candidate"


class UserRegisterSchema(BaseModel):
    # ── common fields ────────────────────────────
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.candidate
    phone_no: Optional[str] = None

    # ── HR-specific: inline org data ─────────────
    organization: Optional[OrganizationInlineSchema] = None

    # ── Candidate-specific ────────────────────────
    skills: Optional[List[str]] = None
    experience: Optional[float] = None          # years

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()

    @model_validator(mode="after")
    def validate_role_fields(self) -> "UserRegisterSchema":
        if self.role == UserRole.hr and not self.organization:
            raise ValueError("HR users must provide organization details")
        return self


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class OrganizationEmbedSchema(BaseModel):
    """Embedded organization details returned inside user response."""
    id: str
    name: str
    industry: str
    size: Optional[int]
    location: str


class UserResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    role: str
    phone_no: Optional[str] = None
    organization_id: Optional[str] = None
    organization: Optional[OrganizationEmbedSchema] = None  # populated on lookup
    skills: Optional[List[str]] = None
    experience: Optional[float] = None
    created_at: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema

