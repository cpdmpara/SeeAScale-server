from fastapi import APIRouter, HTTPException, Depends
from service.CommentService import CommentService, CommentServiceException
from dto.CommentDto import CommentCreateRequestDto, CommentResponseDto
from utils.request_manager import get_log_in_token
from utils.crypto_manager import encode_id, decode_id

router = APIRouter(prefix="/comment", tags=["comment"])

@router.post("/{thingId:str}")
def create(request: CommentCreateRequestDto, thingId: str, logInToken = Depends(get_log_in_token), service: CommentService = Depends()):
    try:
        comment = service.create(request.content, decode_id(thingId), decode_id(logInToken["accountId"]))
    except CommentServiceException.NotFoundThing:
        raise HTTPException(status_code=404)
    
    comment.commentId = encode_id(comment.commentId)
    comment.createrId = encode_id(comment.createrId)
    response = CommentResponseDto(**comment.model_dump())
    return response
