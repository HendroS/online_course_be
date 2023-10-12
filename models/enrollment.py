from sqlalchemy import ForeignKey,text,select,func
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from . import db

class Enrollment(db.Model):
    __tablename__='enrollment'
    user_id:Mapped[int]= mapped_column(ForeignKey("users.user_id"),primary_key=True)
    course_id:Mapped[str] = mapped_column(ForeignKey("courses.course_id"),primary_key=True)
    is_completed:Mapped[bool] = mapped_column(db.Boolean,nullable=False,default=False)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)

    
    def __repr__(self):
        return f'<Enrollment {self.user_id} {self.course_id}>'
    

    
    @classmethod
    def get_by_user_id(cls,id):
        return cls.query.filter_by(user_id = id).all()
    
    @classmethod
    def get_by_course_id(cls,id):
        return cls.query.filter_by(course_id = id).all()
    
    @classmethod
    def get_unique(cls,user_id,course_id):
        return cls.query.filter_by(course_id = course_id,user_id=user_id).first()
    
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

    