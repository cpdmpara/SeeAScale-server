from fastapi import Depends
from sqlalchemy import select
from utils.database import Session, get_db
from utils.entity import Thing, Comment
from datetime import datetime

class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, content: str, thingId: int, createrId: int) -> Comment:
        now = datetime.now()

        comment = Comment(
            content=content,
            createdAt=now,
            modifiedAt=now,
            createrId=createrId,
            thingId=thingId
        )
        self.db.add(comment)
        self.db.flush()
        self.db.refresh(comment)

        return comment
    
    def get_thing(self, thingId: int) -> Thing | None:
        statement = select(Thing).where(Thing.thingId == thingId)
        return self.db.execute(statement).scalar_one_or_none()
    
    def commit(self):
        self.db.commit()
