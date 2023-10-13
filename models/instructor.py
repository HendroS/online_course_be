from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db


class Instructor(db.Model):
    __tablename__='instructors'
    instructor_id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    instructor_name:Mapped[str] = mapped_column(db.String(60), nullable=False)
    description:Mapped[str] = mapped_column(db.Text, nullable=True)
    image:Mapped[str] = mapped_column(db.String(255), nullable=True)
    is_active:Mapped[bool]=mapped_column(db.Boolean,nullable=False,default=True)
    



    def __repr__(self):
        return f'<Instructor {self.instructor_id} {self.instructor_name}>'
    
    @classmethod
    def get_instructor(cls,id):
        return cls.query.filter_by(instructor_id = id).first()
    
    @classmethod
    def get_by_name(cls,name):
        return cls.query.filter_by(instructor_name = name).all()
    
    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_active=True).all()
    
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