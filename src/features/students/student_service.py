from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.core.configs.database import session_scope
from src.core.models import Student


class StudentService:
    def create_student(
        self,
        *,
        student_code: str,
        full_name: str,
        email: str | None = None,
        phone: str | None = None,
        date_of_birth: date | None = None,
        student_class: str | None = None,
    ) -> Student:
        with session_scope() as session:
            row = Student(
                student_code=student_code.strip(),
                full_name=full_name.strip(),
                email=email.strip() if email else None,
                phone=phone.strip() if phone else None,
                date_of_birth=date_of_birth,
                student_class=student_class.strip() if student_class else None,
            )
            session.add(row)
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Mã sinh viên đã tồn tại",
                ) from None
            session.refresh(row)
            session.expunge(row)
            return row

    def list_students(self, *, skip: int = 0, limit: int = 50) -> list[Student]:
        with session_scope() as session:
            rows = (
                session.query(Student)
                .order_by(Student.id.asc())
                .offset(skip)
                .limit(min(limit, 200))
                .all()
            )
            for r in rows:
                session.expunge(r)
            return rows

    def get_student(self, student_id: int) -> Student:
        with session_scope() as session:
            row = session.query(Student).filter(Student.id == student_id).first()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Không tìm thấy sinh viên",
                )
            session.expunge(row)
            return row

    def update_student(
        self,
        student_id: int,
        *,
        student_code: str | None = None,
        full_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        date_of_birth: date | None = None,
        student_class: str | None = None,
    ) -> Student:
        with session_scope() as session:
            row = session.query(Student).filter(Student.id == student_id).first()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Không tìm thấy sinh viên",
                )
            if student_code is not None:
                row.student_code = student_code.strip()
            if full_name is not None:
                row.full_name = full_name.strip()
            if email is not None:
                row.email = email.strip() if email else None
            if phone is not None:
                row.phone = phone.strip() if phone else None
            if date_of_birth is not None:
                row.date_of_birth = date_of_birth
            if student_class is not None:
                row.student_class = student_class.strip() if student_class else None
            try:
                session.commit()
            except IntegrityError:
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Mã sinh viên đã tồn tại",
                ) from None
            session.refresh(row)
            session.expunge(row)
            return row

    def delete_student(self, student_id: int) -> None:
        with session_scope() as session:
            row = session.query(Student).filter(Student.id == student_id).first()
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Không tìm thấy sinh viên",
                )
            session.delete(row)
            session.commit()
