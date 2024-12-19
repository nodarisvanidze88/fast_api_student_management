from sqlalchemy.orm import Session

from app import models, schemas
from .util import check_password,hash_password

def login_user(db: Session, username:str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not check_password(password, user.hashed_password):
        return None
    return user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db:Session):
    return db.query(models.User).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_courses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: schemas.CourseCreate, instructor_id: int):
    db_course = models.Course(**course.model_dump(), instructor_id=instructor_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_lessons(db: Session, course_id: int):
    return db.query(models.Lesson).filter(models.Lesson.course_id == course_id).all()

def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(**lesson.model_dump())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_enrollments(db: Session, user_id: int):
    return db.query(models.Enrollment).filter(models.Enrollment.user_id == user_id).all()

def create_enrollment(db: Session, enrollment: schemas.EnrollmentCreate):
    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment