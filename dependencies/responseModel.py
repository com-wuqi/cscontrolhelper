from pydantic import BaseModel,field_validator, ConfigDict
"""
返回值模型，用于过滤敏感数据
"""
class ResponseUser(BaseModel):
    student_id:int
    name:str
    secret_key:str
    team: str
    is_alive: bool

class ResponseAdmin(BaseModel):
    id:int
    secret_key:str


class PublicStates(BaseModel):
    name: str
    is_alive: bool
    kill: list
    team: str
