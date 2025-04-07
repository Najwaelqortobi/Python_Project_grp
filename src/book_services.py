from .book_repository import *

# Funciones de servicio (no necesitan modificarse)
def get_book_service(book_id):  
    return get_book(book_id)  

def get_all_books_service():  
    return get_all_books()  

def add_book_service(new_book):  
    add_book(new_book)  

def update_book_service(book_id, updated_data):  
    update_book(book_id, updated_data)  

def delete_book_service(book_id):  
    delete_book(book_id)  
