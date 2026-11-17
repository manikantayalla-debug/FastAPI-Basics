
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Student
from app.schemas import StudentCreate, StudentResponse, UpdateDivision


app = FastAPI(title="Student API")


# Create database tables
Base.metadata.create_all(bind=engine)


# HOME
@app.get("/")
def home():
    return {
        "message": "Welcome to Student API"
    }


# HEALTH CHECK
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "student-api"
    }


# ASSIGNMENT 1: ABOUT
@app.get("/about", status_code=200)
def get_about():
    return {
        "project": "Student API",
        "version": "1.0",
        "created_by": "Manikanta Yalla"
    }


# ASSIGNMENT 2: COURSES
@app.get("/courses", status_code=200)
def get_courses():
    return {
        "courses": [
            "Python",
            "DBMS",
            "Computer Networks",
            "Data Structures"
        ]
    }


# ASSIGNMENT 3:
# Pydantic validates incoming request data.
# Invalid data returns 422 Unprocessable Entity.


# ASSIGNMENT 4: CRUD OPERATIONS


# Q1: GET ALL STUDENTS
@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    return students


# Q2: GET STUDENT BY ROLL NUMBER
@app.get("/student/{roll_no}", response_model=StudentResponse)
def get_student(roll_no: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.roll_no == roll_no
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# Q3: CREATE STUDENT
@app.post(
    "/student/",
    status_code=201,
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    # Check whether roll number already exists
    existing_student = db.query(Student).filter(
        Student.roll_no == student.roll_no
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Roll number already exists"
        )

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


# Q4: UPDATE STUDENT DIVISION
@app.patch("/students/{roll_no}", status_code=200)
def update_division(
    roll_no: int,
    update: UpdateDivision,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.roll_no == roll_no
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.division = update.division

    db.commit()
    db.refresh(student)

    return {
        "message": "Division updated successfully!",
        "Student": student
    }


# Q5: DELETE STUDENT
@app.delete("/student/{roll_no}", status_code=204)
def delete_student(
    roll_no: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.roll_no == roll_no
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return Response(status_code=204)
