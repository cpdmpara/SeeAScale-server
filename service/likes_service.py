from fastapi import Depends
from repository.likes_repository import LikesRepository
from utils.service_exception import AlreadyLiked

class LikesService:
    def __init__(self, repository: LikesRepository = Depends()) -> None:
        self.repository = repository
    
    def create(self, userId: int, thingId: int):
        likes = self.repository.get(userId, thingId)

        if likes:
            raise AlreadyLiked()
        
        self.repository.create(userId, thingId)
        self.repository.db.commit()