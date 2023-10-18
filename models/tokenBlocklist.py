from uuid import uuid4
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db
from datetime import datetime

class TokenBlocklist(db.Model):
    __tablename__='token_blocklist'
    id:Mapped[uuid4]= mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    jti:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Blocklist {self.jti}>'
    
    @classmethod
    def get_by_jti(cls,jti):
        return cls.query.filter_by(jti=jti).first()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    