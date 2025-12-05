from fastapi import HTTPException, Form, Cookie
from utils.crypto_manager import verify_token
from utils.constant import COOKIE_LOG_IN

class RequestManagerException:
    class NotLoggedIn(Exception): pass

def get_log_in_token(logInToken: str | None = Cookie(None, alias=COOKIE_LOG_IN)) -> dict:
    if logInToken is None:
        raise RequestManagerException.NotLoggedIn()
    return verify_token(logInToken)