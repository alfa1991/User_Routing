from pydantic import BaseModel

# Схемы для пользователей
class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int

    class Config:
        orm_mode = True


# Схемы для задач
class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

    class Config:
        orm_mode = True


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int

    class Config:
        orm_mode = True


class TaskResponse(BaseModel):
    id: int
    title: str
    content: str
    priority: int
    completed: bool

    class Config:
        orm_mode = True
