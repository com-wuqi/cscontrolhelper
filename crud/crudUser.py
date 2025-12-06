from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..dependencies.secureHelper import *
from ..depends import get_logger
from sqlmodel import select,update

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
        logger.info(f"created user: {users.student_id}")
        session.refresh(users)
    except sqlalchemy.exc.IntegrityError:
        states = 1
        session.rollback()
        logger.warning(f"user already exists: {users.student_id}")


    return states



def add_secret_key_by_id(student_id:int,session: SessionDep):
    statement = select(User).where(User.student_id == student_id)
    user = session.exec(statement).first()
    user.secret_key = generate_secret_key()
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.student_id} added secret key")
        session.refresh(user)
        return user.secret_key
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.student_id} could not add secret key")
        return False

def get_user_by_student_id(student_id:int,session: SessionDep):
    statement = select(User).where(User.student_id == student_id)
    user = session.exec(statement).first()
    return user

def change_user_alive_by_id(student_id:int,alive:bool,session: SessionDep):
    statement = select(User).where(User.student_id == student_id)
    user = session.exec(statement).first()
    user.is_alive = alive
    session.add(user)
    try:
        session.commit()
        logger.info(f"user: {user.student_id} changed statues")
        session.refresh(user)
        return user.is_alive
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        logger.warning(f"user: {user.student_id} could not change statues")
        return None


def add_kill_info(student_id: int, killed_student_id: int, session: SessionDep):
    try:

        statement = select(User).where(User.student_id == student_id).with_for_update()
        user = session.exec(statement).one()  # 确保用户存在，否则抛出异常

        # user.kill = literal_eval(str(user.kill))

        if killed_student_id in user.kill:
            logger.info(f"Kill record for {killed_student_id} already exists for user {student_id}")
            return user.kill


        new_kill_list = user.kill.copy()  # 创建新列表避免引用问题
        new_kill_list.append(killed_student_id)

        update_stmt = (
            update(User)
            .where(User.student_id == student_id)
            .values(kill=json.dumps(new_kill_list))
            .execution_options(synchronize_session="fetch")
        )
        session.exec(update_stmt)
        session.commit()
        session.refresh(user)

        logger.info(f"User {student_id} added kill: {killed_student_id}. New kills: {user.kill}")
        return user.kill
    except Exception as e:
        logger.exception(f"Unexpected error updating kills for user {student_id}: {str(e)}")
        session.rollback()
        return None
