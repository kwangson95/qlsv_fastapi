from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    student_code: str = Field(..., min_length=1, max_length=64)
    full_name: str = Field(..., min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    date_of_birth: date | None = None
    student_class: str | None = Field(default=None, max_length=128)


class StudentUpdate(BaseModel):
    student_code: str | None = Field(default=None, min_length=1, max_length=64)
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=32)
    date_of_birth: date | None = None
    student_class: str | None = Field(default=None, max_length=128)


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_code: str
    full_name: str
    email: str | None
    phone: str | None
    date_of_birth: date | None
    student_class: str | None
    created_at: datetime | None
    updated_at: datetime | None
