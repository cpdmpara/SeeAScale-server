from fastapi import APIRouter, Depends
from service.account_service import AccountService
from model.account_model import PreregisterRequest, AccountCreateRequest, LoginRequest
from utils.preprocessor import get_login_token

router = APIRouter(prefix="/account", tags=["/account"])

@router.post("/preregister")
def preregister(request: PreregisterRequest, service: AccountService = Depends()):
    return service.preregister(request=request)

@router.get("/preverify")
def verify_pretoken(pretoken: str, service: AccountService = Depends()):
    return service.verify_pretoken(pretoken=pretoken)

@router.post("")
def create(request: AccountCreateRequest, service: AccountService = Depends()):
    return service.create(request=request)

@router.post("/login")
def login(request: LoginRequest, service: AccountService = Depends()):
    return service.login(request=request)

@router.post("/logout")
def logout(service: AccountService = Depends()):
    return service.logout()

@router.get("/info")
def get(login_token: dict = Depends(get_login_token), service: AccountService = Depends()):
    return service.get(login_token=login_token)
