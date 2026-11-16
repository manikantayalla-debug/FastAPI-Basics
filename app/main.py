from fastapi import FastAPI
from pydantic import BaseModel,Field

app = FastAPI(title="Student API")

@app.get("/")
def home():
    return {
        "message" : "Welcome to Student API"
    }

class StudentCreate(BaseModel):
    name : str = Field(min_length=2,max_length=100)
    division : str

@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "service" : "student-api"
    }

@app.post("/students",status_code=201)
def create_student(student: StudentCreate):
    return {
        "message" : "Student received Sucessfully!",
        "student" : student
    }

#Assignment 1
@app.get("/about",status_code=200)
def get_about():
    return{
        "project" : "Student API",
        "version" : "1.0",
        "created_by" : "Manikanta Yalla"
    }

#Assignment 2
@app.get("/courses",status_code=200)
def get_courses():
    return {
            "courses" : [
                "Pythton",
                "DBMS",
                "Computer Networkds",
                "Data Structures"
            ]
    }

#Assignment 3
"""The key value pair must match name of the attribute in BaseModel as well as pass its validation test cases. If either one of them isn't passed it will throw error 422 Unprocessable Content"""

#Assignment 4

class Student(BaseModel):
    roll_no :int = Field(gt=0)
    name : str = Field(min_length=2, max_length=100)
    division : str = Field(min_length=1)


students = [{"roll_no" : 101, "name" : "Manikanta", "division" : "B"}]

#Q1
@app.get("/students",status_code=200)
def get_students():
    return{
        "Students" : students
    }

#Q2
@app.get("/student/{roll_no}",status_code=200)
def get_student(roll_no: int):
    student = None
    for s in students:
        if s["roll_no"] == roll_no:
            student = s
            break
    

    return {
        "Student" : student
    }

#Q3
@app.post("/student/",status_code=201)
def create_student(student : Student):
    students.append(student.model_dump())
    return {
        "message" : "Student received Successfully!",
        "Student" : student
    }


#Q4

class UpdateDivision(BaseModel):
    division : str = Field(min_length=1)

@app.patch("/students/{roll_no}",status_code=200)
def update_division(roll_no : int, update : UpdateDivision):

    for student in students:
        if student["roll_no"] == roll_no:
            student["division"] = update.division

            return {
                "message" : "Division Updated Sucessfully!",
                "Student" : student
            }

    return{ "message" : "Student not found!"
    }

#Q5
@app.delete("/student/{roll_no}",status_code=204)
def delete_student(roll_no : int):

    for i,student in enumerate(students):
        if student["roll_no"] == roll_no:
            students.pop(i)
            return