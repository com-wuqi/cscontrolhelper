from datetime import datetime

from pydantic import BaseModel
"""
返回值模型，用于过滤敏感数据
"""
class ResponseUser(BaseModel):
    id:int
    is_active: bool
    email:str
    name:str
    secret_key:str
    last_login:datetime