from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.env import env


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = env.get('DATABASE_LOGIN_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
