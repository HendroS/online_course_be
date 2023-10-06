from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db

class Role(db.Model):
    __tablename__='roles'
    role_id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    role_name:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    description:Mapped[str] = mapped_column(db.String(60), nullable=True)
    users= db.relationship('User',backref='role',lazy=True)
    
    def __repr__(self):
        return f'<role {self.role_name}>'