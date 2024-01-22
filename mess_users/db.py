from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from mess_users.constants import *

# engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
engine = create_engine('sqlite:///mess-users.db')
session = Session(bind=engine)
