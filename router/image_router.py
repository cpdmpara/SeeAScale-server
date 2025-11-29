from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from utils.crypto_manager import decode_id
from utils.constant import IMAGE_STORAGE_PATH
import os

router = APIRouter(prefix="/image", tags=["image"])

@router.get("/{thingId:str}")
def get(thingId: str):
    thingId = decode_id(thingId)

    if os.path.isfile(f"{IMAGE_STORAGE_PATH}/{thingId}.jpeg"):
        return FileResponse(f"{IMAGE_STORAGE_PATH}/{thingId}.jpeg")
    
    raise HTTPException(status_code=404)