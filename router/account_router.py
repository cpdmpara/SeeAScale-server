from fastapi import APIRouter, Cookie, Depends
from service.account_service import AccountService
from model.account_model import PreregisterRequest, AccountCreateRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["/auth"])

@router.post("/preregister")
def preregister(request: PreregisterRequest, service: AccountService = Depends()):
    return service.preregister(request.email)

@router.get("/preverify")
def verify_pretoken(pretoken: str, service: AccountService = Depends()):
    return service.verify_pretoken(pretoken)

@router.post("/register")
def create_account(request: AccountCreateRequest, service: AccountService = Depends()):
    return service.create_account(request)

@router.post("/login")
def login(request: LoginRequest, service: AccountService = Depends()):
    return service.login(request)

@router.post("/logout")
def login(service: AccountService = Depends()):
    return service.logout()

@router.get("/info")
def get_login_info(login_token: str | None = Cookie(default=None), service: AccountService = Depends()):
    return service.get_login_info(login_token)
