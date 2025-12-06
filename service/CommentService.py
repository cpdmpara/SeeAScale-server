from fastapi import Depends
from repository.CommentRepository import CommentRepository, Comment
from dto.CommentDto import CommentInternalDto

class CommentServiceException:
    class NotFoundThing(Exception): pass

class CommentService:
    def __init__(self, repository: CommentRepository = Depends()):
        self.repository = repository
    
    def create(self, content: str, thingId: int, createrId: int) -> CommentInternalDto:
        thing = self.repository.get_thing(thingId)
        if thing is None: raise CommentServiceException.NotFoundThing()

        comment = self.repository.create(content, thing, createrId)

        result = comment_to_internal_dto(comment)

        self.repository.commit()
        return result

    def get_list(self, thingId: int) -> list[CommentInternalDto]:
        comments = self.repository.get_list(thingId)
        if comments is None: raise CommentServiceException.NotFoundThing()

        result = [comment_to_internal_dto(comment) for comment in comments]

        return result

def comment_to_internal_dto(comment: Comment) -> CommentInternalDto:
    result = CommentInternalDto.model_validate(comment)
    result.createrName = comment.creater.name
    return result
