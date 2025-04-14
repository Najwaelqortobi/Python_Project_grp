from .book_repository import *

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

def get_all_authors_service():  
    return get_all_authors()  

def get_author_service(author_id):  
    return get_author(author_id)  


def add_author_service(new_author):  
    add_author(new_author)  

def delete_author_service(author_id):  
    delete_author(author_id)  

def get_books_authors():
    return get_books_rela()