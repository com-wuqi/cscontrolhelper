from fastapi import APIRouter,Request
import asyncio
from ..depends import get_logger,event_generator,message_queue
from fastapi.responses import StreamingResponse
from time import time


router = APIRouter()
logger = get_logger(__name__)


@router.get("/api/public/sse")
async def sse_endpoint(request: Request):
    """SSE 端点"""

    async def event_stream():
        try:
            async for event in event_generator():
                if await request.is_disconnected():
                    logger.warning("sse disconnected")
                    break
                yield event
        except asyncio.CancelledError:
            logger.warning("sse canceled")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

# @router.post("/api/admin/push")
async def push_message(message: str):
    """推送消息到所有连接的客户端"""
    await message_queue.put({
        "timestamp": time(),
        "message": message,
    })
    return {"status": "message queued"}
