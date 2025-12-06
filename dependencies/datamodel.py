from typing import List
from ast import literal_eval

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
            return str(value)
        return "[]"

    def process_result_value(self, value, dialect):
        if value is not None:
            return literal_eval(value)
        return []

class User(SQLModel,table=True):
    __tablename__ = "user"
    id: int = Field(default=None, primary_key=True)
    student_id: int = Field(index=True, nullable=False,unique=True)
    name: str = Field(index=True, nullable=False)
    is_alive: bool = Field(default=True, nullable=False)  # 是否活着
    secret_key: str = Field(index=False,nullable=True)  # 登录凭证,由后端生成
    password: str = Field(index=False, nullable=False)  # str
    kill: List[int] = Field(
        default_factory=list,
        sa_type=ListOfIntegers,
        nullable=False  # 显式声明非空
    )  # 击杀统计,内容为 student_id
    team: str = Field(index=True,nullable=False,default="")  # 队伍,由后端分配 ("red","blue")


class Admin(SQLModel, table=True):
    __tablename__ = "admin"
    id: int = Field(default=None, primary_key=True)
    user: str = Field(index=True, nullable=False,unique=True)
    password: str = Field(index=False, nullable=False)
    secret_key: str = Field(index=False,nullable=True)  # 登录凭证,由后端生成



