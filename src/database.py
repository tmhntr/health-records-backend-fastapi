from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils import env_get


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = env_get('DATABASE_LOGIN_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
