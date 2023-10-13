from sqlalchemy import ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship
from datetime import datetime
from . import db

class Enrollment(db.Model):
    __tablename__='enrollment'

    enrollment_id:Mapped[int]= mapped_column(db.Integer,autoincrement=True,primary_key=True)
    user_id:Mapped[int]= mapped_column(ForeignKey("users.user_id"),nullable=False)
    course_id:Mapped[str] = mapped_column(ForeignKey("courses.course_id"),nullable=False)
    is_completed:Mapped[bool] = mapped_column(db.Boolean,nullable=False,default=False)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)

    enrollment_details= relationship('EnrollmentDetail',backref='enrollment',lazy=True) 

    __table_args__ = (
        UniqueConstraint(user_id, course_id, name='unique_user_course'),
    )

    
    def __repr__(self):
        return f'<Enrollment {self.user_id} {self.course_id}>'
    

    
    @classmethod
    def get_by_user_id(cls,id)->list:
        return cls.query.filter_by(user_id = id).all()
    
    @classmethod
    def get_by_course_id(cls,id)->list:
        return cls.query.filter_by(course_id = id).all()
    
    @classmethod
    def get_unique(cls,user_id,course_id)->list:
        return cls.query.filter_by(course_id = course_id,user_id=user_id).first()
    
    @classmethod
    def get(cls,id):
        return cls.query.filter_by(enrollment_id = id).first()
    
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

    