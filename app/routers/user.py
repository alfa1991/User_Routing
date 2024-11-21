from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..backend.db_depends import (get_db)  # Функция подключения к БД
from typing import Annotated, List
from ..models import User, Task  # Модель пользователя
from ..schemas import CreateUser, UpdateUser  # Схемы Pydantic для создания и обновления пользователей
from sqlalchemy import insert, select, update, delete  # SQLAlchemy для операций с БД
from slugify import slugify  # Функция для создания slug на основе username
from ..schemas import UserResponse, TaskResponse


router = APIRouter(
    prefix="/user",
    tags=["user"]
)



@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks


# Функция получения всех пользователей
@router.get("/", response_model=List[UserResponse])
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


# Функция получения пользователя по ID
@router.get("/{user_id}", response_model=UserResponse)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user


# Функция создания нового пользователя
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user_data = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)  # Создаем slug на основе username
    )
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data  # Возвращаем созданного пользователя


# Функция обновления данных пользователя
@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db_user.firstname = user.firstname
    db_user.lastname = user.lastname
    db_user.age = user.age
    db_user.slug = slugify(user.username)  # Перегенерируем slug, если изменился username

    await db.commit()
    await db.refresh(db_user)
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}


# Функция удаления пользователя
@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).filter(User.id == user_id)).scalar()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db.delete(db_user)
    await db.commit()
    return {"status_code": status.HTTP_204_NO_CONTENT, "transaction": "User deleted successfully"}
