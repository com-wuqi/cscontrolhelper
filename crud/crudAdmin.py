import sqlalchemy.exc
from sqlmodel import select

from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..dependencies.secureHelper import *
from ..depends import get_logger

logger = get_logger(__name__)
"""
数据库操作
"""
def create_user(users:Admin,session: SessionDep) -> int:
    states = 0
    session.add(users)
    try:
        session.commit()
        logger.info(f"created user: {users.id}")
        session.refresh(users)
    except sqlalchemy.exc.IntegrityError:
        states = 1
        session.rollback()
        logger.warning(f"user already exists: {users.id}")


    return states



def add_secret_key_by_id(admin_id:int,session: SessionDep):
    statement = select(Admin).where(Admin.id == admin_id)
    user = session.exec(statement).first()
    user.secret_key = generate_secret_key()
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.id} added secret key")
        session.refresh(user)
        return user.secret_key
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.id} could not add secret key")
        return False

def get_user_by_id(admin_id:int,session: SessionDep):
    statement = select(Admin).where(Admin.id == admin_id)
    user = session.exec(statement).first()
    return user

def get_user_by_username(username:str,session: SessionDep):
    statement = select(Admin).where(Admin.user == username)
    user = session.exec(statement).first()
    return user