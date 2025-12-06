from pydantic import BaseModel
from typing import List
"""
请求体模型
"""
class UserLogin(BaseModel):
    student_id: int
    password: str

class UserRegister(BaseModel):
    name: str
    password: str
    student_id: int


class UserLogout(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    user: str
    password: str

class AdminRegister(BaseModel):
    user: str
    password: str

class ScanAndKill(BaseModel):
    student_id: int
    secret_key: str
    killed_student_id: int

class AdminPushMessage(BaseModel):
    id: int
    secret_key: str
    message: str