from fastapi import APIRouter, UploadFile, File, Depends
from service.thing_service import ThingSerivce
from model.thing_model import ThingCreateRequest, ThingModifyRequest
from utils.preprocessor import thing_create_form, get_login_token

router = APIRouter(prefix="/thing", tags=["thing"])

@router.post("")
async def create(
    request: ThingCreateRequest = Depends(thing_create_form),
    imageFile: UploadFile = File(),
    login_token: dict = Depends(get_login_token),
    service: ThingSerivce = Depends()
):
    return service.create(request=request, imageFile = await imageFile.read(), login_token=login_token)

@router.get("")
def get_list(prefix: int = 0, page: int = 0, service: ThingSerivce = Depends()):
    return service.get_list(prefix, page)

@router.get("/{thingId:str}")
def get(thingId: str, service: ThingSerivce = Depends()):
    return service.get(thingId)

@router.patch("/{thingId:str}")
def update(request: ThingModifyRequest, thingId: str, login_token: dict = Depends(get_login_token), service: ThingSerivce = Depends()):
    return service.update(request, thingId, login_token)

@router.delete("/{thingId:str}")
def delete(thingId: str, login_token: dict = Depends(get_login_token), service: ThingSerivce = Depends()):
    return service.delete(thingId, login_token)