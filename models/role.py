from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db

class Role(db.Model):
    __tablename__='roles'
    role_id:Mapped[uuid4]= mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    role_name:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    description:Mapped[str] = mapped_column(db.String(60), nullable=True)
    users= db.relationship('User',backref='role',lazy=True)
    
    def __repr__(self):
        return f'<role {self.role_name}>'
    
    def get_by_id(cls,id):
        return cls.query.filter_by(role_id=id).first()