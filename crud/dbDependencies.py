from ..depends import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

def get_session_for_background():
    return Session(engine)

SessionDep = Annotated[Session, Depends(get_session)]
