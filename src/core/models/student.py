from datetime import date

from sqlalchemy import INTEGER, Column, Date, DateTime, String, func

from .base import Base


class Student(Base):
    __tablename__ = "student"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    student_code = Column(String(64), nullable=False, unique=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(32), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    student_class = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
