from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Float

engine = create_engine('sqlite:///library.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    nationality = Column(String)
    books = relationship("Book", back_populates="author_rel", lazy='joined') # si quiero definir la relacion en una sola direccion
    #books = relationship("Book", backref="author_rel")  


class Book(Base):
    __tablename__ = 'books'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    year = Column(Integer)
    author_id = Column(String, ForeignKey('authors.id'))
    author_rel = relationship("Author", back_populates="books")  
    sales = relationship("Sale", back_populates="book")  


class Sale(Base):
    __tablename__ = 'sales'
    id = Column(String, primary_key=True)
    book_id = Column(String, ForeignKey('books.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # <-- Float ahora funciona
    book = relationship("Book", back_populates="sales")



