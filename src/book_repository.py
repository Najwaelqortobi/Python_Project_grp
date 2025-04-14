from sqlalchemy.orm import Session
from .models import Base, engine, Author, Book, Sale, SessionLocal 
from sqlalchemy import func

# Inicializar la sesión de la base de datos
def get_db_session():
    return SessionLocal()

# Obtener un libro por ID
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

# Obtener todos los libros
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

# Añadir nuevo libro
def add_book(new_book):
    session = get_db_session()
    try:
        book = Book(
            id=new_book['id'],
            title=new_book['title'],
            year=new_book['year'],
            author_id=new_book['author_id']  # Asegúrate de incluir esto
        )
        session.add(book)
        session.commit()
    except Exception as e:
        print(f"Error en add_book: {str(e)}")
        session.rollback()
        raise  # Propaga el error para verlo en los logs
    finally:
        session.close()

# Actualizar libro
def update_book(book_id, updated_data):
    session = get_db_session()
    try:
        book = session.query(Book).filter_by(id=book_id).first()
        if book:
            book.title = updated_data.get('title', book.title)
            book.year = updated_data.get('year', book.year)
            book.author_id = updated_data.get('author_id', book.author_id)
            session.commit()
    except Exception as e:
        print(f"Error en update_book: {str(e)}")
        session.rollback()
    finally:
        session.close()

# Eliminar libro
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
            "total_books": len(author.books)  
        } for author in authors]  
    finally:  
        session.close()  

# Obtener un autor por ID
def get_author(author_id):  
    session = get_db_session()  
    try:  
        author = session.query(Author).filter_by(id=author_id).first()  
        return {  
            "id": author.id,  
            "name": author.name,  
            "nationality": author.nationality,  
            "books": [book.title for book in author.books]  
        } if author else None  
    finally:  
        session.close()  

# Añadir nuevo autor
def add_author(new_author):  
    session = get_db_session()  
    try:  
        author = Author(  
            id=new_author['id'],  
            name=new_author['name'],  
            nationality=new_author.get('nationality')  
        )  
        session.add(author)  
        session.commit()  
    except Exception as e:  
        print(f"Error en add_author: {str(e)}")  
        session.rollback()  
    finally:  
        session.close()  

# Eliminar autor
def delete_author(author_id):  
    session = get_db_session()  
    try:  
        author = session.query(Author).filter_by(id=author_id).first()  
        if author:  
            session.query(Book).filter_by(author_id=author_id).delete()  
            session.delete(author)  
            session.commit()  
    except Exception as e:  
        print(f"Error en delete_author: {str(e)}")  
        session.rollback()  
    finally:  
        session.close()  

# Obtener relación libros-autores
def get_books_rela():  
    session = get_db_session()  
    try:  
        books = session.query(Book).join(Author).all()  
        return [{  
            "id": book.id,  
            "title": book.title,  
            "year": book.year,  
            "author": {  
                "name": book.author_rel.name,  
                "nationality": book.author_rel.nationality  
            }  
        } for book in books]  
    except Exception as e:  
        print(f"Error en get_books_rela: {str(e)}")  
        return []  
    finally:  
        session.close()  

# Obtener porcentaje de ventas por autor
def get_sales_porcentage():
    session = get_db_session()
    try:
        # Subconsulta para el total de ventas
        total_subquery = session.query(func.sum(Sale.quantity * Sale.price)).scalar() or 0

        # Consulta principal
        query = session.query(
            Author.name,
            func.sum(Sale.quantity * Sale.price).label('total_sales'),
            func.round(func.sum(Sale.quantity * Sale.price) * 100.0 / total_subquery, 2).label('porcentage')
        ).join(Book, Author.books)\
         .join(Sale, Book.sales)\
         .group_by(Author.id)\
         .all()

        return [
            {
                "author": author,
                "porcentage de ventas": f"{porcentage}%"
            }
            for author, _, porcentage in query
        ]
    except Exception as e:
        print(f"Error en get_sales_porcentage: {str(e)}")
        return []
    finally:
        session.close()


# Inicializar base de datos
def init_db():  
    from .models import Base, engine, Author, Book, Sale  # Importación corregida
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = get_db_session()  
    try:  
        # Autores de prueba
        autores = [  
            Author(id='A1', name='Gabriel García Márquez', nationality='Colombiana'),  
            Author(id='A2', name='George Orwell', nationality='Británica'),  
            Author(id='A3', name='J.K. Rowling', nationality='Británica'),
            Author(id='A4', name='Isabel Allende', nationality='Chilena'),
            Author(id='A5', name='Haruki Murakami', nationality='Japonés') 
        ]  
        session.bulk_save_objects(autores)  

        # Libros de prueba
        libros = [  
            Book(id='1', title='Cien años de soledad', year=1967, author_id='A1'),  
            Book(id='2', title='1984', year=1949, author_id='A2'),  
            Book(id='3', title='Harry Potter y la piedra filosofal', year=1997, author_id='A3'),
            Book(id='4', title='La casa de los espíritus', year=1982, author_id='A4'),
            Book(id='5', title='Tokio Blues', year=1987, author_id='A5'),
        ]  
        session.bulk_save_objects(libros)  

        # Ventas de prueba
        ventas = [
            Sale(id='S1', book_id='1', quantity=150, price=25.99),
            Sale(id='S2', book_id='2', quantity=300, price=19.99),
            Sale(id='S3', book_id='3', quantity=500, price=29.99),
        ]
        session.bulk_save_objects(ventas)
        session.commit()
    finally:
        session.close()
