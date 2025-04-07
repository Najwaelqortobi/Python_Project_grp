from flask import Flask, request, jsonify  
from flask_cors import CORS  
from .book_services import *  

app = Flask(__name__)  
CORS(app)  

# Inicializar base de datos  
from .book_repository import init_db  
init_db()  

@app.route("/books", methods=["GET"])  #si queremos leer los libros en el post tenemos que poner http://127.0.0.1:9000/books
def all_books_route():  
    books = get_all_books_service()  
    return jsonify(books)  #jsonify es una función de Flask que convierte datos Python en respuestas JSON válidas para APIs. 

@app.route("/books/<book_id>", methods=["GET"])  
def get_book_route(book_id):  
    book = get_book_service(book_id)  
    return jsonify(book) if book else ("Libro no encontrado", 404)  

@app.route("/books/<book_id>", methods=["DELETE"])  
def delete_book_route(book_id):  
    delete_book_service(book_id)  
    return "", 204  

@app.route("/books", methods=["POST"])    #si queremos agregar un libro en el post tenemos que poner http://127.0.0.1:9000/books
def new_book_route():  
    new_book = request.get_json()  
    add_book_service(new_book)  
    return "", 201  

@app.route("/books/<book_id>", methods=["PUT"])  #si queremos agregar un libro en el post tenemos que poner http://127.0.0.1:9000/books/id del book que quiero modificar 
def update_book_route(book_id):  
    updated_data = request.get_json()  
    update_book_service(book_id, updated_data)  
    return "", 200  

@app.route("/", methods=["GET"])  
def hello():  
    return "API de Biblioteca"  