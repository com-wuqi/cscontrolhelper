import asyncio
import json
import logging
from os import getenv
from typing import AsyncGenerator

from sqlmodel import create_engine

from .dependencies.datamodel import *

use_sqlite = getenv("USE_SQLITE",default="yes")
use_mysql = getenv("USE_MYSQL",default="yes")

if use_mysql == "yes":
    mysql_uri = getenv("DATABASE_URL", "")
    if mysql_uri == "":
        raise ValueError("DATABASE_URL is required when USE_MYSQL=yes")

    connect_args = {"charset": "utf8mb4","connect_timeout": 10}
    engine = create_engine(
        mysql_uri,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=True,  # 输出 SQL 日志（调试用）
        pool_size=10,  # 连接池大小
        max_overflow=15,  # 最大溢出连接数
    )
elif use_sqlite == "yes":
    sqlite_uri = getenv("SQLALCHEMY_DATABASE_URI",default="sqlite:///sqlite0.db")
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_uri, connect_args=connect_args)
else:
    raise ValueError("Unsupported SQLAlchemy engine type")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    # danger!!!!
    SQLModel.metadata.drop_all(engine)

def get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger

message_queue = asyncio.Queue()


async def event_generator() -> AsyncGenerator[str, None]:
    """事件生成器"""
    while True:
        # 等待新消息
        message = await message_queue.get()
        if message == "CLOSE":
            break

        # 格式化SSE消息
        yield f"data: {json.dumps(message)}\n\n"
        await asyncio.sleep(0.1)  # 避免过载

