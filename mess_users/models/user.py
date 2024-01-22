from sqlalchemy import Boolean, String
from sqlalchemy.orm import mapped_column, Mapped

from mess_users import helpers
from mess_users.models import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String(32), primary_key=True, unique=True, default=helpers.uuid)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
