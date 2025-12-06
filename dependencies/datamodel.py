from typing import List
from datetime import datetime,timezone

import json
from sqlmodel import Field, SQLModel,Relationship,JSON,Column,VARCHAR,TypeDecorator

"""
数据库模型
"""


class ListOfIntegers(TypeDecorator):
    impl = VARCHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value

class User(SQLModel,table=True):
    __tablename__ = "user"
    id: int = Field(default=None, primary_key=True)
    student_id: int = Field(index=True, nullable=False,unique=True)
    name: str = Field(index=True, nullable=False)
    is_alive: bool = Field(default=True, nullable=False)  # 是否活着
    secret_key: str = Field(index=False,nullable=True)  # 登录凭证,由后端生成
    password: str = Field(index=False, nullable=False)  # str
    kill: List[int] = Field(
        default=[],
        sa_column=Column(ListOfIntegers)
    )  # 击杀统计,内容为 student_id
    team: str = Field(index=True,nullable=False,default="")  # 队伍,由后端分配 ("red","blue")


class Admin(SQLModel, table=True):
    __tablename__ = "admin"
    id: int = Field(default=None, primary_key=True)
    user: str = Field(index=True, nullable=False,unique=True)
    password: str = Field(index=False, nullable=False)
    secret_key: str = Field(index=False,nullable=True)  # 登录凭证,由后端生成



