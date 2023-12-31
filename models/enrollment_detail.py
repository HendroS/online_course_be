from datetime import datetime
from uuid import uuid4
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db



class EnrollmentDetail(db.Model):
    __tablename__='enrollment_detail'
    enrollment_id:Mapped[uuid4]= mapped_column(ForeignKey("enrollment.enrollment_id"),primary_key=True)
    chapter_id:Mapped[uuid4]= mapped_column(ForeignKey("chapter.chapter_id"),primary_key=True)
    is_completed:Mapped[bool]= mapped_column(db.Boolean,nullable=False,default=False)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow,nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)


    def __repr__(self):
        return f'<EnrollmentDetail {self.enrollment_id} {self.chapter_id}>'
    
    @classmethod
    def get_enrollment(cls,enroll_id):
        return cls.query.filter_by(enrollment_id=enroll_id).all()
    
    @classmethod
    def get_by_chapter(cls,chapter_id):
        return cls.query.filter_by(chapter_id = chapter_id).all()
    
    @classmethod
    def get_unique(cls,enrollment_id,chapter_id):
        return cls.query.filter_by(enrollment_id=enrollment_id,chapter_id=chapter_id).first()

    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    def completed(self):
        self.is_completed = True
        self.updated_at = datetime.utcnow()
        db.session.commit()

    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
