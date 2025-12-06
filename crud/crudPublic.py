from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..depends import get_logger
from sqlmodel import select



logger = get_logger(__name__)

def get_users(session: SessionDep,offset:int,limit:int):
    query = select(User)
    users = session.exec(query.limit(limit).offset(offset)).all()
    return users