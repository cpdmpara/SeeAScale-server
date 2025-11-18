from fastapi import FastAPI
from router import root
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(root.router)
