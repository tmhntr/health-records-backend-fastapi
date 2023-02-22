from authlib.integrations.starlette_client import OAuthError
from jose import JWTError, jwt
from starlette.responses import RedirectResponse
from fastapi import Request

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.dependencies import get_db
from app.auth import authenticate_user, create_access_token, oauth


router = APIRouter(
    responses={404: {"description": "Not found"}},
    tags=["auth"],
)



@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    

# from fastapi import Depends, HTTPException


@router.route('/login/google')
async def login(request: Request):
    # This creates the url for the /auth endpoint
    redirect_uri = request.url_for('auth_google')
    oauth.fetch_token
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.route('/auth/google/callback')
async def auth_google(request: Request):
    try:
        oauth.fetch_token
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    # return user_data in jwt format
    access_token = create_access_token(data={"sub": user_data['email'], "user_id": user_data['sub']})
    return {"access_token": access_token, "token_type": "bearer"}


    