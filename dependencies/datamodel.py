from typing import List
from datetime import datetime,timezone


from sqlmodel import Field, SQLModel,Relationship,JSON,Column,VARCHAR

"""
数据库模型
"""

class UserBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=False, nullable=False)
    email: str = Field(index=True,unique=True)
    password: str = Field(index=True)
    # 永远不要存储用户的明文密码，也不要在响应中发送密码。
    password_salt: str = Field(index=True, nullable=False)
    is_active: bool = Field(default=True)
    # 是否存活
    last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    secret_key: str = Field(index=False)
    is_banned: bool = Field(default=False)
    # 凭据
    # 用户拥有的资源权限

class User(UserBase, table=True):
    __tablename__ = "user"
    kill: List[int] = Field(
        default_factory=list,
        sa_column=Column(VARCHAR)
    )


class AdminUser(UserBase, table=True):
    __tablename__ = "adminuser"
    is_superuser: bool = Field(default=False) # 最高权限


