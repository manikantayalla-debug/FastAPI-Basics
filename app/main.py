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