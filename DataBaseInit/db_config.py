from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from manage_db import create_db_user, get_database_url


DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

create_db_user('api', 'Passw0rd')
