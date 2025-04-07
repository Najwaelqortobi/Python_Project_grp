import sqlite3
from flask import jsonify

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row  # Acceso por nombres de columna
    return conn

# Operaciones CRUD
def get_book(book_id):
    conn = get_db_connection()
    try:
        book = conn.execute(
            'SELECT * FROM books WHERE id = ?', (book_id,)
        ).fetchone()
        return dict(book) if book else None
    finally:
        conn.close()

def get_all_books():
    conn = get_db_connection()
    try:
        books = conn.execute('SELECT * FROM books').fetchall()
        return [dict(book) for book in books]
    finally:
        conn.close()

def add_book(new_book):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?)',
            (new_book['id'], new_book['title'], new_book['author'], new_book['year'])
        )
        conn.commit()
    finally:
        conn.close()

def update_book(book_id, updated_data):
    conn = get_db_connection()
    try:
        conn.execute(
            '''UPDATE books
            SET title = ?, author = ?, year = ?
            WHERE id = ?''',
            (updated_data['title'], updated_data['author'], updated_data['year'], book_id)
        )
        conn.commit()
    finally:
        conn.close()

def delete_book(book_id):
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
    finally:
        conn.close()

# Crear tabla si no existe y poblar con datos iniciales
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
    ''')
    
    # Verificar si la tabla está vacía
    cursor = conn.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:  # Si no hay registros
        # Insertar libros de ejemplo
        libros_ejemplo = [
            ('1', 'Cien años de soledad', 'Gabriel García Márquez', 1967),
            ('2', '1984', 'George Orwell', 1949),
            ('3', 'Don Quijote de la Mancha', 'Miguel de Cervantes', 1605),
            ('4', 'El principito', 'Antoine de Saint-Exupéry', 1943)
        ]
        conn.executemany(
            'INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?)',
            libros_ejemplo
        )
        conn.commit()
        print("✅ 4 libros insertados en la base de datos")
    else:
        print("ℹ️ La base de datos ya contiene registros")
    
    conn.close()