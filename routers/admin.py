from secrets import compare_digest

from fastapi import APIRouter, HTTPException

from .sse import push_message
from ..crud import crudAdmin, crudUser, crudPublic
from ..crud.dbDependencies import SessionDep
from ..dependencies import requestModel, secureHelper
from ..dependencies.datamodel import *
from ..dependencies.responseModel import *
from ..depends import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/api/admin/login",response_model=ResponseAdmin)
async def user_login(data: requestModel.AdminLogin, session: SessionDep):
    user = crudAdmin.get_user_by_username(username=data.user, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    input_passwd = secureHelper.hash_salted_password(data.password)
    if compare_digest(input_passwd, user.password):
        crudAdmin.add_secret_key_by_id(admin_id=user.id, session=session)
        return user
    else:
        raise HTTPException(status_code=403, detail="Incorrect Password")



@router.post("/api/admin/register")
async def user_register(data: requestModel.AdminRegister, session: SessionDep):
    user_password = data.password
    user_name = data.user
    user_secret_key = secureHelper.generate_secret_key()
    hashed_password = secureHelper.hash_salted_password(user_password)
    user = Admin(
        user=user_name,
        password=hashed_password,
        secret_key=user_secret_key,
    )

    states = crudAdmin.create_user(user, session)
    if states == 0:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="user already exists!")

@router.post("/api/admin/sseSend")
async def sse_send(data: requestModel.AdminPushMessage, session: SessionDep):
    admin = crudAdmin.get_user_by_id(data.id,session=session)
    if admin is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not compare_digest(data.secret_key, admin.secret_key):
        raise HTTPException(status_code=403, detail="Incorrect secret key")
    await push_message(message=data.message)
    return {"message": "message sent successfully"}

@router.post("/api/admin/resurrect")
async def resurrect(data: requestModel.AdminResurrect, session: SessionDep):
    admin = crudAdmin.get_user_by_id(data.id, session=session)
    if admin is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not compare_digest(data.secret_key, admin.secret_key):
        raise HTTPException(status_code=403, detail="Incorrect secret key")
    states = crudUser.change_user_alive_by_id(student_id=data.student_id,alive=True,session=session)
    if states is None:
        raise HTTPException(status_code=500, detail="could not change user statues")
    return {"message": "message resurrected successfully"}

@router.post("/api/admin/changeGameStatus")
async def change_game_status(data: requestModel.AdminChangeGameStatus, session: SessionDep):
    # admin = crudAdmin.get_user_by_id(data.id, session=session)
    # if admin is None:
    #     raise HTTPException(status_code=404, detail="User does not exist")
    # if not compare_digest(data.secret_key, admin.secret_key):
    #     raise HTTPException(status_code=403, detail="Incorrect secret key")
    config = crudPublic.get_game_config(session=session)
    config.is_started = data.game_status
    session.commit()
    session.refresh(config)
    if config.is_started:
        msg = "游戏开始"
    else:
        msg = "游戏停止"
    await push_message(message=msg)
    return {"game_statues": f"{config.is_started}"}

