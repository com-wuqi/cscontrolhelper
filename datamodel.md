# data_model 文档

## user_data 玩家
id: int = Field(default=None, primary_key=True)

student_id: int = Field(index=True, nullable=False)

name: str = Field(index=True, nullable=False)

is_alive: bool = Field(default=True,nullable=False) # 是否活着

secret_key: str = Field(index=False) # 登录凭证,由后端生成

password: str = Field(index=False,nullable=False) # str

kill: List[int] = Field(
        default_factory=list,
        sa_column=Column(VARCHAR)
) # 击杀统计,内容为 student_id

team: str = Field(index=True) # 队伍,由后端分配 ("red","blue")

## admin_data 管理员
id: int = Field(default=None, primary_key=True)

user: str: = Field(index=True, nullable=False)

password: str = Field(index=False,nullable=False)

secret_key: str = Field(index=False) # 登录凭证,由后端生成

