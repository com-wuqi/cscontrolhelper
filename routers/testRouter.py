from fastapi import APIRouter
from ..crud.dbDependencies import SessionDep
from ..depends import get_logger
router = APIRouter()
logger = get_logger(__name__)

@router.get("/test/dependency")
async def test_dependency(session: SessionDep):
    return {
        "session_works": session is not None,
        "session_type": type(session).__name__
    }

@router.get("/test/logger")
async def test_logger(logger_type: str, message: str):
    if logger_type == "info":
        logger.info(message)
    elif logger_type == "warning":
        logger.warning(message)
    elif logger_type == "error":
        logger.error(message)
    elif logger_type == "debug":
        logger.debug(message)
    else:
        logger.critical(message)
    return {"message": message}
