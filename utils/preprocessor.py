from fastapi import HTTPException, Form, Cookie
from model.thing_model import ThingCreateRequest
from utils.token_manager import verify_token
from utils.constant import LOGIN_TOKEN_COOKIE

def get_login_token(login_token: str | None = Cookie(None, alias=LOGIN_TOKEN_COOKIE)) -> dict:
    if login_token is None:
        raise HTTPException(status_code=401, detail="NOT_LOGINED")
    return verify_token(login_token)

def thing_create_form(thingName: str = Form(), prefix: int = Form(), quantity: str = Form(), explaination: str = Form()) -> ThingCreateRequest:
    try:
        return ThingCreateRequest(thingName=thingName, prefix=prefix, quantity=quantity, explaination=explaination)
    except:
        raise HTTPException(status_code=422)