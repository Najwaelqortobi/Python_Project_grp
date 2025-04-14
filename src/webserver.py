from flask import Flask, request, jsonify  
from flask_cors import CORS  
from .book_services import *  

app = Flask(__name__)  
CORS(app)  

# Inicializar la base de datos
from .book_repository import init_db  
init_db()  

# Endpoints
@app.route("/books", methods=["GET"])  
def all_books_route():  
    books = get_all_books_service()  
    return jsonify(books)  

@app.route("/books/<book_id>", methods=["GET"])  
def get_book_route(book_id):  
    book = get_book_service(book_id)  
    return jsonify(book) if book else ("Libro no encontrado", 404)  

@app.route("/books/<book_id>", methods=["DELETE"])  
def delete_book_route(book_id):  
    delete_book_service(book_id)  
    return "", 204  

@app.route("/books", methods=["POST"])  
def new_book_route():  
    new_book = request.get_json()  
    add_book_service(new_book)  
    return "", 201  

@app.route("/books/<book_id>", methods=["PUT"])  
def update_book_route(book_id):  
    updated_data = request.get_json()  
    update_book_service(book_id, updated_data)  
    return "", 200  


# Endpoints para autores  
@app.route("/authors", methods=["GET"])  
def all_authors_route():  
    authors = get_all_authors_service()  
    return jsonify(authors)  

@app.route("/authors/<author_id>", methods=["GET"])  
def get_author_route(author_id):  
    author = get_author_service(author_id)  
    return jsonify(author) if author else ("Autor no encontrado", 404)  



# Crear autor  
@app.route("/authors", methods=["POST"])  
def new_author_route():  
    new_author = request.get_json()  
    add_author_service(new_author)  
    return "", 201  

# Eliminar autor  
@app.route("/authors/<author_id>", methods=["DELETE"])  
def delete_author_route(author_id):  
    delete_author_service(author_id)  
    return "", 204  


# Mostrar relación autor-libros  
@app.route("/books/rela", methods=["GET"])  
def books_with_authors_route():  
    books = get_books_authors()  # Usa el servicio existente  
    return jsonify(books)  

#Mostrar porcentage de ventas
@app.route("/sales/porcentage", methods=["GET"])
def sales_porcentage_route():
    sales_data = get_sales_porcentage()
    return jsonify(sales_data)

@app.route("/", methods=["GET"])  
def hello():  
    return "API de Biblioteca"  



# Archivo de entrada (main.py)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000)  # Permite conexiones desde cualquier IP
