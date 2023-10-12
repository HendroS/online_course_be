from sqlalchemy import ForeignKey, text
from . import db
import bcrypt

from sqlalchemy.orm import Mapped, mapped_column,relationship

class User(db.Model):
    __tablename__='users'
    user_id:Mapped[int]= mapped_column(db.Integer, primary_key=True,autoincrement=True)
    username:Mapped[str] = mapped_column(db.String, nullable=False,unique=True)
    email:Mapped[str] = mapped_column(db.String, nullable=False,unique=True)
    password:Mapped[str] = mapped_column(db.String(60), nullable=False)
    role_id:Mapped[int] = mapped_column(ForeignKey("roles.role_id"), nullable=False,default=2)

    enrolls= relationship("Enrollment",backref='user',lazy=True)
    user_chapters= relationship('UserChapter',backref='user',lazy=True)



    def __repr__(self):
        return f'<user {self.username}>'
    
    def set_password(self,password:str):
        hashed= bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        self.password=hashed.decode('utf-8')
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))
    
    @classmethod
    def get_user_by_email(cls,email):
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def get_user_by_id(cls,id):
        return cls.query.filter_by(user_id = id).first()
    
    @classmethod
    def get_user_by_username(cls,username):
        return cls.query.filter_by(username = username).first()
    
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

    @classmethod
    def get_top_enrolled(cls,numbers=5):
        q=text(
            f"SELECT t.user_id,u.username,t.qty \
            from (SELECT e.user_id , COUNT(e.user_id) qty  FROM enrollment e\
               GROUP BY e.user_id) t\
               JOIN users u ON u.user_id = t.user_id\
               ORDER BY qty DESC\
                LIMIT {numbers}"
               )     

        result= db.engine.connect().execute(q).mappings().all()
        print(result)
        return result
    
