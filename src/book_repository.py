from sqlalchemy.orm import Session
from .models import Book, SessionLocal

def get_db_session():
    return SessionLocal()

def get_book(book_id):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        } if book else None
    except Exception as e:
        print(f"Error en get_book: {str(e)}")
        return None
    finally:
        session.close()

def get_all_books():
    session = get_db_session()
    try:
        books = session.query(Book).all()
        return [{
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year
        } for book in books]
    except Exception as e:
        print(f"Error en get_all_books: {str(e)}")
        return []
    finally:
        session.close()

def add_book(new_book):
    session = get_db_session()
    try:
        book = Book(**new_book)
        session.add(book)
        session.commit()
    except Exception as e:
        print(f"Error en add_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

def update_book(book_id, updated_data):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        if book: #aqui no esta permitido cambiar el id de un libro si queremos hacerlo  tenemos que agregar la linea :
            #if 'id' in updated_data:
                #book.id = updated_data['id']
            book.title = updated_data.get('title', book.title)
            book.author = updated_data.get('author', book.author)
            book.year = updated_data.get('year', book.year)    
          
            session.commit()
    except Exception as e:
        print(f"Error en update_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

def delete_book(book_id):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            session.delete(book)
            session.commit()
    except Exception as e:
        print(f"Error en delete_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

def init_db():
    from .models import Base, engine
    Base.metadata.create_all(engine)  # Crear tablas aquí
    
    session = get_db_session()
    try:
        if session.query(Book).count() == 0:
            libros_ejemplo = [
                Book(id='1', title='Cien años de soledad', author='Gabriel García Márquez', year=1967),
                Book(id='2', title='1984', author='George Orwell', year=1949),
                Book(id='3', title='Don Quijote de la Mancha', author='Miguel de Cervantes', year=1605),
                Book(id='4', title='El principito', author='Antoine de Saint-Exupéry', year=1943)
            ]
            session.bulk_save_objects(libros_ejemplo)
            session.commit()
            print("✅ 4 libros insertados en la base de datos")
        else:
            print("ℹ️ La base de datos ya contiene registros")
    except Exception as e:
        print(f"Error en init_db: {str(e)}")
    finally:
        session.close()
