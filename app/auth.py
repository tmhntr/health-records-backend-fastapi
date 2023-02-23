from fastapi import Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from app import schemas

from app.env import env, set_up


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token_auth_scheme = HTTPBearer()  # 👈 new code


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up(())

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload

# # OAuth settings
# GOOGLE_CLIENT_ID = env.get('GOOGLE_CLIENT_SECRET') or None
# GOOGLE_CLIENT_SECRET = env.get('GOOGLE_CLIENT_ID') or None
# if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
#     raise BaseException('Missing env variables')

# # Set up oauth
# config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
#                'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
# config = Config(environ=config_data)
# oauth = OAuth(config)

# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
# oauth.register(
#     name='google',
#     server_metadata_url=CONF_URL,
#     client_kwargs={
#         'scope': 'openid email profile'
#     }
# )

# create secret key with command: openssl rand -hex 32
SECRET_KEY = env.get("SECRET_KEY")
ALGORITHM = "HS256"







def create_access_token(data: dict, expires_delta=timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


