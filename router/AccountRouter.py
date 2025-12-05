from fastapi import APIRouter, Response, HTTPException, Depends
from service.AccountService import AccountService, AccountServiceException
from dto.AccountDto import AccountPreregisterRequestDto, AccountCreateRequestDto
from utils.crypto_manager import create_token, verify_token, encode_id
from utils.constant import RELEASE, ALREADY_REGISTERED, INVALID_TOKEN, EXPIRED_TOKEN, COOKIE_LOG_IN, SIGN_UP_TOKEN_EXPIRY_PERIOD

router = APIRouter(prefix="/prefix", tags=["prefix"])

@router.post("/preregister")
def preregister(request: AccountPreregisterRequestDto, service: AccountService = Depends()):
    try:
        service.preregister(request.email, request.name, request.password)
    except AccountServiceException.AreadyRegisteredEmail:
        raise HTTPException(status_code=409, detail=ALREADY_REGISTERED)
    
    response = Response(status_code=200)
    return response

@router.post("")
def create(request: AccountCreateRequestDto, service: AccountService = Depends()):
    try:
        account = service.create(request.signUpToken)
    except AccountServiceException.InvalidSignupToken:
        raise HTTPException(status_code=401, detail=INVALID_TOKEN)
    except AccountServiceException.ExpiredSignupToken:
        raise HTTPException(status_code=401, detail=EXPIRED_TOKEN)
    except AccountServiceException.AreadyRegisteredEmail:
        raise HTTPException(status_code=409, detail=ALREADY_REGISTERED)

    logInToken = create_token(
        {
            "accountId": encode_id(account.accountId),
            "name": account.name
        },
        expire=SIGN_UP_TOKEN_EXPIRY_PERIOD
    )

    response = Response(status_code=201)
    response.set_cookie(
        key=COOKIE_LOG_IN,
        value=logInToken,
        max_age=SIGN_UP_TOKEN_EXPIRY_PERIOD,
        httponly=True,
        secure=RELEASE,
        samesite="strict"
    )
    
    return response