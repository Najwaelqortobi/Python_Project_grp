from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de SQLAlchemy (conexión a SQLite)
engine = create_engine('sqlite:///library.db')
SessionLocal = sessionmaker(bind=engine)  # Renombrado para evitar conflictos
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
