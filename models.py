from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
Base = declarative_base()
#Many-to-One Relationship
class Author(Base,SerializerMixin):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    books = relationship("Book", back_populates="author")


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            # 'books': [book.serialize() for book in self.books]
        }

    @classmethod
    def serialize_list(cls, authors):
        return [author.serialize() for author in authors]

class Book(Base,SerializerMixin):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="books")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.title,
            'author': self.author.serialize()
        }

    @classmethod
    def serialize_list(cls, books):
        return [book.serialize() for book in books]
