from pydantic import BaseModel
from typing import List
"""
请求体模型
"""
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    name: str
    password: str
    password_salt: str

class UserLogout(BaseModel):
    email: str
    password: str

