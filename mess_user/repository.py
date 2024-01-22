from typing import Optional

from mess_user.db import session
from mess_user.models.user import User


def get_user(user_id: str) -> Optional[User]:
    return session.query(User).filter(User.id == user_id).first()


def create_user(username: str) -> User:
    user = User(username=username)
    session.add(user)
    session.commit()

    return user


def delete_user(user_id: str) -> None:
    session.query(User).filter(User.id == user_id).delete()
    session.commit()


def username_exists(username: str) -> bool:
    return session.query(User).filter(User.username == username).first() is not None


def search_users(username: str) -> list[User]:
    return session.query(User).filter(User.username.like(f"%{username}%")).all()
