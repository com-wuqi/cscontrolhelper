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


@router.post("/api/user/login", response_model=ResponseUser)
async def user_login(data: requestModel.UserLogin, session: SessionDep):
    pass
    # user_email = data.email  # 用户输入的邮箱
    # input_passwd = data.password  # 用户输入的密码
    # user = crudUser.get_user_by_email(user_email, session)
    # if user is None:
    #     logger.warning(f"user with email {user_email} does not exist")
    #     raise HTTPException(status_code=403, detail="Incorrect email or password")
    # if user.is_banned:
    #     logger.warning(f"user with email {user_email} banned but try to login again")
    #     raise HTTPException(status_code=403, detail="Incorrect email or password")
    # user_passwd_salt = user.password_salt  # 数据库中的密码盐
    # salt_passwd = secureHelper.hash_salted_password(input_passwd)  # 加盐后的用户输入
    # hashed_password = user.password  # 数据库中的密码
    # if not compare_digest(salt_passwd, hashed_password):
    #     logger.warning(f"user with email {user_email} failed to login")
    #     raise HTTPException(status_code=403, detail="Incorrect email or password")
    # key = crudUser.add_secret_key_by_id(user.id, session)
    # if key is False:
    #     logger.warning(f"user with email {user_email} failed to add a new key")
    #     raise HTTPException(status_code=500, detail="could not add a new key")
    # update_is_active = crudUser.update_is_active_and_time_by_id(user.id, True, session)
    # if update_is_active is False:
    #     logger.warning(f"user with email {user_email} failed to update the status")
    #     raise HTTPException(status_code=500, detail="could not update the status")
    # return user


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


