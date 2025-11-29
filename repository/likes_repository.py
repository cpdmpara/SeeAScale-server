from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.schema import Likes

class LikesRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, userId: int, thingId: int) -> Likes:
        likes = Likes(userId=userId, thingId=thingId)

        self.db.add(likes)

        return likes

    def get(self, userId: int, thingId: int) -> Likes | None:
        statement = select(Likes).where(and_(Likes.userId == userId, Likes.thingId == thingId))
        return self.db.execute(statement).scalar_one_or_none()
    
    def delete(self, userId: int, thingId: int) -> None:
        statement = select(Likes).where(and_(Likes.userId == userId, Likes.thingId == thingId))
        likes = self.db.execute(statement).scalar_one_or_none()
        self.db.delete(likes)