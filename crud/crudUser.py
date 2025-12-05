from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..depends import get_logger
from sqlmodel import select
from datetime import datetime,timezone
import sqlalchemy.exc
logger = get_logger(__name__)
"""
数据库操作
"""
def create_user(users:User,session: SessionDep) -> int:
    states = 0
    session.add(users)
    try:
        session.commit()
        logger.info(f"created user: {users.email}")
        session.refresh(users)
    except sqlalchemy.exc.IntegrityError:
        states = 1
        session.rollback()
        logger.warning(f"email already exists: {users.email}")


    return states

def get_user_by_email(users_email:str,session: SessionDep):
    user = session.exec(select(User).where(User.email == users_email)).first()
    session.refresh(user)
    return user

def add_secret_key_by_id(user_id:int,session: SessionDep):
    user = session.get(User,user_id)
    user.secret_key = ""
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.email} added secret key")
        session.refresh(user)
        return user.secret_key
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.email} could not add secret key")
        return False

def update_is_active_and_time_by_id(user_id:int,is_active:bool,session: SessionDep):
    """
    用于登录
    """
    user = session.get(User,user_id)
    user.is_active = is_active
    user.last_login = datetime.now(timezone.utc)
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.email} updated status")
        session.refresh(user)
        return user.is_active
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.email} could not update status")
        return False

def user_logout(user_id:int,session: SessionDep):
    user = session.get(User,user_id)
    user.is_active = False
    user.last_login = datetime.now(timezone.utc)
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.email} logged out")
        session.refresh(user)
        return user.is_active
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.email} could not logout")
        return -1