from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db



class UserChapter(db.Model):
    __tablename__='user_chapter'
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"),primary_key=True)
    chapter_id:Mapped[int]= mapped_column(ForeignKey("chapter.chapter_id"),primary_key=True)
    is_completed:Mapped[bool]= mapped_column(db.Boolean,nullable=False,default=False)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)


    def __repr__(self):
        return f'<UserChapter {self.user_id} {self.chapter_id}>'
    
    @classmethod
    def get_by_user(cls,user_id):
        return cls.query.filter_by(user_id = user_id).all()
    
    @classmethod
    def get_by_chapter(cls,chapter_id):
        return cls.query.filter_by(chapter_id = chapter_id).all()
    
    @classmethod
    def get_unique(cls,user_id,chapter_id):
        return cls.query.filter(user_id=user_id,chapter_id=chapter_id).first()

    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
