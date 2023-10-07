from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from . import db

class Course(db.Model):
    __tablename__='courses'
    course_id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    category_id:Mapped[int]= mapped_column(ForeignKey("categories.category_id"), nullable=False)
    course_name:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    description:Mapped[str] = mapped_column(db.String, nullable=True)
    is_active:Mapped[str]= mapped_column(db.Boolean,nullable=False,default=True)
    
    
    def __repr__(self):
        return f'<Course {self.course_name}>'
    
    @classmethod
    def get_course_by_id(cls,id):
        return cls.query.filter_by(course_id = id).first()
    
    @classmethod
    def get_course_by_name(cls,course_name):
        return cls.query.filter_by(course_name = course_name).first()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_all_with_active_status(cls,is_active:bool):
        return cls.query.filter_by(is_active=is_active).all()
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
