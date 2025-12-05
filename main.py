from fastapi import FastAPI
from utils.middleware import exception_catcher
from router import AccountRouter

app = FastAPI()

app.middleware("http")(exception_catcher)

app.include_router(AccountRouter.router)