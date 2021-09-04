from sqlalchemy.orm import DeclarativeMeta, Session


def create_in_storage(db_session: Session, obj: DeclarativeMeta):
    db_session.add(obj)
    db_session.flush()
    db_session.refresh(obj)
