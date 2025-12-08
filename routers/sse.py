import asyncio
import json
from time import time

from fastapi import APIRouter, Request
# from ..depends import event_generator,message_queue
from fastapi.responses import StreamingResponse

from ..depends import get_logger, sse_manager

router = APIRouter()
logger = get_logger(__name__)


@router.get("/api/public/sse")
async def sse_endpoint(request: Request):
    """SSE 端点 - 支持多用户订阅"""
    # 1. 注册新订阅者
    client_queue, client_id = await sse_manager.subscribe()

    async def event_stream():
        try:
            while True:
                # 2. 从客户端专属队列获取消息
                event = await client_queue.get()

                # 3. 检查连接状态
                if await request.is_disconnected():
                    logger.warning(f"客户端 {client_id} 主动断开")
                    break

                yield event

        except asyncio.CancelledError:
            logger.warning(f"客户端 {client_id} 被取消")
        finally:
            # 4. 确保清理资源
            await sse_manager.unsubscribe(client_id)

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用Nginx缓冲
            "Content-Type": "text/event-stream",
        }
    )

# @router.post("/api/test/push")
async def push_message(message: str):
    """推送消息到所有连接的客户端"""
    msg = {"time": str(time()), "message": message}
    data = str(json.dumps(msg))
    await sse_manager.broadcast(data)
    logger.info(f"push message:{data}")
    return {"status": "message queued"}
