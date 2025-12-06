from fastapi import APIRouter, HTTPException
from ..dependencies import requestModel, secureHelper
from ..dependencies.datamodel import *
from ..dependencies.responseModel import *
from ..crud.dbDependencies import SessionDep
from ..crud import crudUser
from ..depends import get_logger
from secrets import compare_digest

router = APIRouter()
logger = get_logger(__name__)


@router.post("/api/player/login", response_model=ResponseUser)
async def user_login(data: requestModel.UserLogin, session: SessionDep):
    user = crudUser.get_user_by_student_id(student_id=data.student_id, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")
    input_passwd = secureHelper.hash_salted_password(data.password)
    if compare_digest(input_passwd, user.password):
        crudUser.add_secret_key_by_id(student_id=data.student_id, session=session)
        return user
    else:
        raise HTTPException(status_code=403, detail="Incorrect Password")



@router.post("/api/player/register")
async def user_register(data: requestModel.UserRegister, session: SessionDep):
    user_password = data.password
    user_name = data.name
    user_secret_key = secureHelper.generate_secret_key()
    hashed_password = secureHelper.hash_salted_password(user_password,)
    user = User(
        name=user_name,
        password=hashed_password,
        student_id=data.student_id,
        secret_key=user_secret_key,
        kill=[]
    )

    states = crudUser.create_user(user, session)
    if states == 0:
        return {"message": "User created successfully"}
    else:
        raise HTTPException(status_code=400, detail="user already exists!")


@router.post("/api/player/scan")
async def user_player_scan(data: requestModel.ScanAndKill, session: SessionDep):
    user = crudUser.get_user_by_student_id(student_id=data.student_id, session=session)
    if not user.is_alive:
        raise HTTPException(status_code=403, detail="User was killed")
    if not compare_digest(user.secret_key, data.secret_key):
        raise HTTPException(status_code=403, detail="Incorrect secret_key")
    killed_user = crudUser.get_user_by_student_id(student_id=data.killed_student_id, session=session)
    if killed_user is None:
        raise HTTPException(status_code=404, detail="killedUser does not exist")
    if compare_digest(user.team, killed_user.team):
        raise HTTPException(status_code=403, detail="could not kill the same group members")
    states = crudUser.change_user_alive_by_id(student_id=data.killed_student_id,alive=False,session=session)
    if states is None:
        raise HTTPException(status_code=403, detail="Failed to change alive status")
    else:
        add_info = crudUser.add_kill_info(student_id=data.student_id, killed_student_id=data.killed_student_id,session=session)
        if add_info is None:
            raise HTTPException(status_code=500, detail="Failed to change alive status")
        # 预留sse
        #
        return {"message": f"{user.student_id} killed {killed_user.student_id}"}