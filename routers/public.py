from fastapi import APIRouter
from ..dependencies.responseModel import *
from ..crud.dbDependencies import SessionDep
from ..crud import crudPublic,crudUser
from ..depends import get_logger


router = APIRouter()
logger = get_logger(__name__)

@router.get("/api/public/status",response_model=list[PublicStates])
async def get_users_status(session: SessionDep,offset:int = 0,limit:int = 1000):
    users = crudPublic.get_users(session,offset,limit)
    return users

@router.get("/api/public/getNameById")
async def get_name_public(student_id: int ,session: SessionDep):
    users = crudUser.get_user_by_student_id(student_id=student_id,session=session)
    return {"name":users.name}