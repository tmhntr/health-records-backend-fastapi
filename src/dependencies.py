from fastapi.security import OAuth2PasswordBearer

# local imports
from src.database import SessionLocal

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://dev-mx-lf095.us.auth0.com/oauth/token")



