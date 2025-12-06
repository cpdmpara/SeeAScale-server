from fastapi import Depends
from repository.CommentRepository import CommentRepository
from dto.CommentDto import CommentInternalDto

class CommentServiceException:
    class NotFoundThing(Exception): pass

class CommentService:
    def __init__(self, repository: CommentRepository = Depends()):
        self.repository = repository
    
    def create(self, content: str, thingId: int, createrId: int) -> CommentInternalDto:
        if self.repository.get_thing(thingId) is None: raise CommentServiceException.NotFoundThing()

        comment = self.repository.create(content, thingId, createrId)

        result = CommentInternalDto.model_validate(comment)
        result.createrName = comment.creater.name

        self.repository.commit()
        return result
