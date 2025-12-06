from pydantic import BaseModel
from typing import List
"""
请求体模型
"""
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    password: str
    student_id: int


class UserLogout(BaseModel):
    email: str
    password: str

