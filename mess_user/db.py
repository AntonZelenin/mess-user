from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mess_user import settings

engine = create_engine(settings.get_settings().db_url)
session = Session(bind=engine)
