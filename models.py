from sqlalchemy import String, Integer, Column, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ =  'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(250), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True)
    category_name = Column(String(250), nullable=False)
    user_id = Column(Integer(), ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'category': self.category_name,
        }


class ClassName(Base):
    __tablename__ = 'class'

    id = Column(Integer(), primary_key=True)
    class_name = Column(String(250), nullable=False)
    description = Column(Text(), nullable=False)
    category_id = Column(Integer(), ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer(), ForeignKey('user.id'))
    user = relationship(User)
    
    def serialize(self):
        return {
            'id': self.id,
            'class_name': self.class_name,
            'description':self.description,
            'category': self.category,
            
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)

