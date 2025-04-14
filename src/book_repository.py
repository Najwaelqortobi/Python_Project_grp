from sqlalchemy.orm import Session
from .models import Book, Author, SessionLocal

def get_db_session():
    return SessionLocal()

# Get single book
def get_book(book_id):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        return {
            "id": book.id,
            "title": book.title,
            "year": book.year,
            "nationality": book.author_rel.nationality
        } if book else None
    except Exception as e:
        print(f"Error en get_book: {str(e)}")
        return None
    finally:
        session.close()

# Get all books
def get_all_books():
    session = get_db_session()
    try:
        books = session.query(Book)
        return [{
            "id": book.id,
            "title": book.title,
            "year": book.year,
        } for book in books]
    except Exception as e:
        print(f"Error en get_all_books: {str(e)}")
        return []
    finally:
        session.close()

# Add new book
def add_book(new_book):
    session = get_db_session()
    try:
        book = Book(
            id=new_book['id'],
            title=new_book['title'],
            year=new_book['year']
        )
        session.add(book)
        session.commit()
    except Exception as e:
        print(f"Error en add_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

# Update book
def update_book(book_id, updated_data):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            book.title = updated_data.get('title', book.title)
            book.year = updated_data.get('year', book.year)
            session.commit()
    except Exception as e:
        print(f"Error en update_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

# Delete book
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

        # Obtener todos los autores  
def get_all_authors():  
    session = get_db_session()  
    try:  
        authors = session.query(Author).all()  
        return [{  
            "id": author.id,  
            "name": author.name,  
            "nationality": author.nationality,  
            "total_books": len(author.books)  # Relación con libros/Accede a la lista de libros asociados al autor (gracias a lazy='joined').
        } for author in authors]  
    finally:  
        session.close()  
def get_author(author_id):  
    session = get_db_session()  
    try:  
        author = session.query(Author).filter_by(id=author_id).first()  
        return {  
            "id": author.id,  
            "name": author.name,  
            "nationality": author.nationality,  
 # Libros del autor  
        } if author else None  
    finally:  
        session.close()  


def add_author(new_author):  
    session = get_db_session()  
    try:  
        author = Author(  
            id=new_author['id'],  
            name=new_author['name'],  
            nationality=new_author.get('nationality')  # Opcional  
        )  
        session.add(author)  
        session.commit()  
    except Exception as e:  
        print(f"Error en add_author: {str(e)}")  
        session.rollback()  
    finally:  
        session.close()  
def delete_author(author_id):  
    session = get_db_session()  
    try:  
        author = session.query(Author).filter_by(id=author_id).first()  
        if author:  
            # Elimina los libros asociados primero (evita errores de FK)  
            session.query(Book).filter_by(author_id=author_id).delete()  
            session.delete(author)  
            session.commit()  
    except Exception as e:  
        print(f"Error en delete_author: {str(e)}")  
        session.rollback()  
    finally:  
        session.close()  


#relacion entre books y authors 
def get_books_rela():  
    session = get_db_session()  
    try:  
        books = session.query(Book).join(Author).all()  
        return [{  
            "id": book.id,  
            "title": book.title,  
            "year": book.year,  
            "author": {  # Incluye detalles completos del autor   
                "name": book.author_rel.name,  
            }  
        } for book in books]  
    except Exception as e:  
        print(f"Error en get_all_books: {str(e)}")  
        return []  
    finally:  
        session.close()  



# Initialize database
def init_db():  
    from .models import Base, engine, Author, Book  
    Base.metadata.drop_all(engine)  # ¡Elimina tablas existentes!  
    Base.metadata.create_all(engine)  # Crea tablas desde cero  

    session = get_db_session()  
    try:  
        # Inserta autores (sin verificar si ya existen)  
        autores = [  
            Author(id='A1', name='Gabriel García Márquez', nationality='Colombiana'),  
            Author(id='A2', name='George Orwell', nationality='Británica'),  
            Author(id='A3', name='J.K. Rowling', nationality='Británica'),
            Author(id='A4', name='Isabel Allende', nationality='Chilena'),
            Author(id='A5', name='Haruki Murakami', nationality='Japonés') 

        ]  
        session.bulk_save_objects(autores)  

        # Inserta libros (sin verificar si ya existen)  
        libros = [  
            Book(id='1', title='Cien años de soledad', year=1967, author_id='A1'),  
            Book(id='2', title='1984', year=1949, author_id='A2'),  
            Book(id='3', title='Harry Potter y la piedra filosofal', year=1997, author_id='A3'),
            Book(id='4', title='La casa de los espíritus', year=1982, author_id='A4'),
            Book(id='5', title='Tokio Blues', year=1987, author_id='A5'),

        ]  
        session.bulk_save_objects(libros)  

        session.commit()  
    finally:  
        session.close()  

