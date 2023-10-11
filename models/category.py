from sqlalchemy.orm import Mapped, mapped_column
from . import db
from datetime import datetime

class Category(db.Model):
    __tablename__='categories'
    category_id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    category_name:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    description:Mapped[str] = mapped_column(db.Text, nullable=True)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column(db.DateTime, nullable=True)

    courses= db.relationship('Course',backref='category',lazy=True)
    
    def __repr__(self):
        return f'<Category {self.category_name}>'
    
    @classmethod
    def get_category_by_id(cls,id):
        return cls.query.filter_by(category_id = id).first()
    @classmethod
    def get_category_by_name(cls,name):
        return cls.query.filter_by(category_name = name).first()
    
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