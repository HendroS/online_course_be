from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db
from datetime import datetime

class TokenBlocklist(db.Model):
    __tablename__='token_blocklist'
    id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    jti:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    created_at:Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<Blocklist {self.jti}>'
    
    @classmethod
    def get_by_jti(cls,jti):
        return cls.query.filter_by(jti=jti).first()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    