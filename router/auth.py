from fastapi import APIRouter, Response, Depends
from fastapi.responses import JSONResponse
from model.dto import PreRegisterDTO, RegisterDTO
from service.auth import (
    verify_email_format,
    check_email_register_status,
    send_auth_mail,
    verify_token,
    verify_user_name_format,
    verify_password_format,
    register_user,
    create_login_token,
    InvalidSignatureError,
    ExpiredSignatureError
)
from database import get_db

LOGIN_EXPIRE_PERIOD = 24 * 60 * 60

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def post_preregister(data: PreRegisterDTO, db=Depends(get_db)):
    if not verify_email_format(data.email):
        return JSONResponse({"code":"INVALID_EMAIL_FORMAT"}, status_code=400)
    
    if check_email_register_status(data.email, db):
        return JSONResponse({"code":"ALREADY_REGISTERED_EMAIL"}, status_code=400)
    
    send_auth_mail(data.email)

    return Response()

@router.get("/preverify")
def get_preverify(pretoken: str, db=Depends(get_db)):
    try:
        verify_token(pretoken)
    except InvalidSignatureError:
        return JSONResponse({"code":"INVALID_TOKEN"}, status_code=401)
    except ExpiredSignatureError:
        return JSONResponse({"code":"EXPIRED_TOKEN"}, status_code=401)

    return Response()

@router.post("/register")
def post_register(data: RegisterDTO, db=Depends(get_db)):
    try:
        token_payload = verify_token(data.pretoken) # {"email":"{이메일}", "exp":"{만료시간}"}
    except InvalidSignatureError:
        return JSONResponse({"code":"INVALID_TOKEN"}, status_code=401)
    except ExpiredSignatureError:
        return JSONResponse({"code":"EXPIRED_TOKEN"}, status_code=401)
    
    if not verify_user_name_format(data.user_name):
        return JSONResponse({"code":"INVALID_USER_NAME"}, status_code=400)
    
    if not verify_password_format(data.password):
        return JSONResponse({"code":"INVALID_PASSWORD"}, status_code=400)
    
    if check_email_register_status(token_payload["email"], db):
        return JSONResponse({"code":"ALREADY_REGISTERED_EMAIL"}, status_code=400)
    
    new_account = register_user(token_payload["email"], data.user_name, data.password, db)
    login_token = create_login_token(new_account.user_id, LOGIN_EXPIRE_PERIOD)

    response = Response()
    response.set_cookie(
        key="login_token",
        value=login_token, 
        max_age=LOGIN_EXPIRE_PERIOD,
        httponly=True,
        samesite="strict"
    )

    return response