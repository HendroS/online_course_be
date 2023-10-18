from uuid import uuid4
from sqlalchemy import UUID, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column,relationship
from . import db

prerequisites = db.Table('prerequisites',
    db.Column('course_id', UUID(as_uuid=True), db.ForeignKey('courses.course_id'), primary_key=True),
    db.Column('prerequisite_id', UUID(as_uuid=True), db.ForeignKey('courses.course_id'), primary_key=True)
)

course_instructor = db.Table('course_instructor',
    db.Column('course_id', UUID(as_uuid=True), db.ForeignKey('courses.course_id'), primary_key=True),
    db.Column('instructor_id', UUID(as_uuid=True), db.ForeignKey('instructors.instructor_id'), primary_key=True)
)

class Course(db.Model):
    __tablename__='courses'
    course_id:Mapped[uuid4]= mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    category_id:Mapped[uuid4]= mapped_column(ForeignKey("categories.category_id"), nullable=False)
    course_name:Mapped[str] = mapped_column(db.String(60), nullable=False,unique=True)
    description:Mapped[str] = mapped_column(db.Text, nullable=True)
    is_active:Mapped[str]= mapped_column(db.Boolean,nullable=False,default=True)

    prerequisites = relationship('Course', 
                                secondary = prerequisites, 
                                primaryjoin = (prerequisites.c.course_id == course_id),
                                secondaryjoin = (prerequisites.c.prerequisite_id == course_id),
                                backref = 'needed_on'
                                )
    instructors=relationship('Instructor', secondary=course_instructor, lazy='subquery',
        backref=db.backref('courses', lazy=True))
    enrolls = relationship("Enrollment",backref='course',lazy=True)
    chapters = relationship('Chapter',backref='course',lazy=True)
    
    
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

    @classmethod
    def get_top_favorite(cls,numbers=5):
        q=text(
            f"SELECT c.course_id,c.course_name,t.qty \
            from (SELECT e.course_id , COUNT(e.course_id) qty  FROM enrollment e\
               GROUP BY e.course_id) t\
               JOIN courses c ON c.course_id = t.course_id\
               ORDER BY qty DESC\
                LIMIT {numbers}"
               )     

        result= db.engine.connect().execute(q).mappings().all()
        # print(result)
        return result
    
