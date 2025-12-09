from sqlmodel import select

from .dbDependencies import SessionDep
from ..dependencies.datamodel import *
from ..depends import get_logger

logger = get_logger(__name__)

def get_users(session: SessionDep,offset:int,limit:int):
    query = select(User)
    users = session.exec(query.limit(limit).offset(offset)).all()
    return users


def get_game_config(session: SessionDep):
    statement = select(GameConfig)
    config = session.exec(statement).first()
    if not config:
        config = GameConfig()
        session.add(config)
        session.commit()
        session.refresh(config)
    return config