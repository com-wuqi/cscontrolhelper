import logging
from asyncio import Queue, Lock
from collections import deque
from os import getenv

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

logger = get_logger(__name__)

class SSEManager:
    def __init__(self):
        self.subscribers = deque()  # 存储所有客户端队列
        self.lock = Lock()  # 保护订阅者列表的锁
        self._counter = 0  # 用于生成唯一客户端ID

    async def subscribe(self) -> tuple[Queue, int]:
        """注册新订阅者，返回专属队列"""
        client_id = self._counter
        self._counter += 1
        queue = Queue(maxsize=100)  # 限制队列大小防内存溢出

        async with self.lock:
            self.subscribers.append((client_id, queue))
            logger.info(f"新订阅者加入 (ID:{client_id}), 当前在线: {len(self.subscribers)}")
        return queue, client_id

    async def unsubscribe(self, client_id: int):
        """移除订阅者"""
        async with self.lock:
            # 通过ID精准移除（避免deque.remove()的O(n)复杂度）
            self.subscribers = deque(
                (cid, q) for cid, q in self.subscribers if cid != client_id
            )
        logger.info(f"订阅者离开 (ID:{client_id}), 剩余: {len(self.subscribers)}")

    async def broadcast(self, message: str):
        """向所有订阅者广播消息"""
        event = f"data: {message}\n\n"  # 标准SSE格式
        dead_clients = []

        async with self.lock:
            for client_id, queue in self.subscribers:
                try:
                    # 非阻塞放入消息，满队列时丢弃旧消息
                    if queue.full():
                        await queue.get()  # 丢弃最旧消息
                    queue.put_nowait(event)
                except Exception as e:
                    logger.error(f"客户端 {client_id} 消息失败: {str(e)}")
                    dead_clients.append(client_id)

        # 清理失效连接
        for cid in dead_clients:
            await self.unsubscribe(cid)


# 全局单例管理器
sse_manager = SSEManager()

