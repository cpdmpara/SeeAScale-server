from fastapi import HTTPException, Form, Cookie
from utils.crypto_manager import verify_token
from dto.ThingDto import ThingCreateRequestDto
from utils.constant import COOKIE_LOG_IN
from decimal import Decimal

class RequestManagerException:
    class NotLoggedIn(Exception): pass

def get_log_in_token(logInToken: str | None = Cookie(None, alias=COOKIE_LOG_IN)) -> dict:
    if logInToken is None:
        raise RequestManagerException.NotLoggedIn()
    return verify_token(logInToken)

async def thing_create_body(
    title: str = Form(min_length=1, max_length=32, examples=["서울_부산"]),
    prefix: int = Form(ge=-10, le=10, examples=["3"]),
    quantity: str = Form(examples=["330"]),
    explanation: str = Form(min_length=0, max_length=500, examples=["서울에서 부산까지"])
) -> ThingCreateRequestDto:
    try:
        result = ThingCreateRequestDto(title=title, prefix=prefix, quantity=Decimal(quantity), explanation=explanation)
        return result
    except:
        raise HTTPException(status_code=422)
