from uuid import uuid4
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db
from datetime import datetime

class Chapter(db.Model):
    __tablename__='chapter'
    chapter_id:Mapped[uuid4]= mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    course_id:Mapped[uuid4] = mapped_column(ForeignKey("courses.course_id"), nullable=False)
    chapter_name:Mapped[str]= mapped_column(db.String(255), nullable=False)
    order:Mapped[int]= mapped_column(db.Integer, nullable=False)
    description:Mapped[str] = mapped_column(db.Text, nullable=True)
    content:Mapped[str] = mapped_column(db.Text, nullable=False)

    image:Mapped[str] = mapped_column(db.String(255), nullable=True)
    is_active:Mapped[bool]=mapped_column(db.Boolean,nullable=False,default=True)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow,nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)

    enrollment_details= relationship('EnrollmentDetail',backref='chapter',lazy=True)
    

    def __repr__(self):
        return f'<Chapter {self.chapter_id} {self.chapter_name}>'
    
    @classmethod
    def get_chapter(cls,id):
        return cls.query.filter_by(chapter_id = id).first()
    
    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter_by(chapter_name = name).all()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_active=True).all()
    
    def softDelete(self):
        self.is_active=False
        db.session.commit()
    
    @classmethod
    def get_all_active_status(cls,is_active:bool):
        return cls.query.filter_by(is_active=is_active).all()
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()