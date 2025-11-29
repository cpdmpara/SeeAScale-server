from fastapi import APIRouter, Response, HTTPException, Depends
from service.likes_service import LikesService
from utils.service_exception import AlreadyLiked
from utils.preprocessor import get_login_token
from utils.crypto_manager import decode_id
from utils.constant import ALREADY_REGISTERED

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("")
def create(thingId: str, login_token = Depends(get_login_token), service: LikesService = Depends()):
    userId = decode_id(login_token["userId"])
    thingId = decode_id(thingId)

    try:
        service.create(userId, thingId)
        return Response(status_code=200)
    except AlreadyLiked:
        raise HTTPException(status_code=409, detail=ALREADY_REGISTERED)

