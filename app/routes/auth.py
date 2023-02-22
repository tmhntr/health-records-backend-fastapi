import logging
from authlib.integrations.starlette_client import OAuthError
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.dependencies import get_db
from app.auth import authenticate_user, oauth


router = APIRouter(
    responses={404: {"description": "Not found"}},
    tags=["auth"],
)



@router.post("/auth", response_model=schemas.Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    if user:
        user_dict = {"email": user.email, "user_id": user.id}
        logging.info(user_dict)
        request.session['user'] = user_dict
    return {"access_token": user.email, "token_type": "bearer"}
    

from starlette.requests import Request

@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = request.url_for('auth_via_google')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google")
async def auth_via_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(
            status_code=401, detail="Token authorization failed: " + error.error
        ) 
    user = token.get('userinfo')
    if user:
        logging.info(dict(user))
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')

@router.route('/logout')
async def logout(request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
# from fastapi import Depends, HTTPException


# @router.route('/login/google')
# async def login(request: Request):
#     # This creates the url for the /auth endpoint
#     redirect_uri = request.url_for('auth_google')
#     oauth.fetch_token
#     return await oauth.google.authorize_redirect(request, redirect_uri)


# @router.route('/auth/google/callback')
# async def auth_google(request: Request):
#     try:
#         oauth.fetch_token
#         access_token = await oauth.google.authorize_access_token(request)
#     except OAuthError:
#         return RedirectResponse(url='/')
#     user_data = await oauth.google.parse_id_token(request, access_token)
#     # return user_data in jwt format
#     access_token = create_access_token(data={"sub": user_data['email'], "user_id": user_data['sub']})
#     return {"access_token": access_token, "token_type": "bearer"}


    