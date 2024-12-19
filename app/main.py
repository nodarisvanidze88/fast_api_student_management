from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine
from app.dependencies import get_db
from typing import List

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/", response_model=schemas.User)
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User or password incorrect")
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[schemas.User])
def get_our_all_students(db: Session = Depends(get_db)):
    return crud.get_all_users(db)

@app.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, instructor_id: int, db: Session = Depends(get_db)):
    return crud.create_course(db=db, course=course, instructor_id=instructor_id)

@app.get("/courses/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

@app.post("/lessons/", response_model=schemas.Lesson)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    return crud.create_lesson(db=db, lesson=lesson)

@app.get("/courses/{course_id}/lessons/", response_model=List[schemas.Lesson])
def read_lessons(course_id: int, db: Session = Depends(get_db)):
    lessons = crud.get_lessons(db, course_id=course_id)
    return lessons

@app.post("/enrollments/", response_model=schemas.Enrollment)
def create_enrollment(enrollment: schemas.EnrollmentCreate, db: Session = Depends(get_db)):
    return crud.create_enrollment(db=db, enrollment=enrollment)

@app.get("/users/{user_id}/enrollments/", response_model=List[schemas.Enrollment])
def read_enrollments(user_id: int, db: Session = Depends(get_db)):
    enrollments = crud.get_enrollments(db, user_id=user_id)
    return enrollments