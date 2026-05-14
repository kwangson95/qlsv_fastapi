from fastapi import APIRouter, Query

from src.api.dto.student import StudentCreate, StudentResponse, StudentUpdate
from src.services.student_service import StudentService

router = APIRouter(tags=["Students"], prefix="/students")
student_service = StudentService()


@router.post("", response_model=StudentResponse)
def create_student(body: StudentCreate) -> StudentResponse:
    row = student_service.create_student(
        student_code=body.student_code,
        full_name=body.full_name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.date_of_birth,
        student_class=body.student_class,
    )
    return StudentResponse.model_validate(row)


@router.get("", response_model=list[StudentResponse])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> list[StudentResponse]:
    rows = student_service.list_students(skip=skip, limit=limit)
    return [StudentResponse.model_validate(r) for r in rows]


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int) -> StudentResponse:
    row = student_service.get_student(student_id)
    return StudentResponse.model_validate(row)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, body: StudentUpdate) -> StudentResponse:
    data = body.model_dump(exclude_unset=True)
    row = student_service.update_student(student_id, **data)
    return StudentResponse.model_validate(row)


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int) -> None:
    student_service.delete_student(student_id)
