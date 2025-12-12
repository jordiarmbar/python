from flask import jsonify, request
from src.config.db import session
from src.models.book import Book


def init_api_routes(app):
    # --- READ (GET): Obtener todos los libros ---
    @app.route('/api/books', methods=['GET'])
    def get_books():
        # Consultamos todos los registros usando el ORM
        books = session.query(Book).all()

        # Convertimos los objetos a una lista de diccionarios (JSON)
        books_list = []
        for book in books:
            books_list.append({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'price': book.price
            })

        return jsonify(books_list)

    # --- READ (GET): Obtener un libro por ID ---
    @app.route('/api/books/<int:book_id>', methods=['GET'])
    def get_book_by_id(book_id):
        # Buscamos por clave primaria
        book = session.query(Book).get(book_id)

        if book is None:
            return jsonify({"error": "Book Not Found"}), 404

        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price
        })

    # --- CREATE (POST): Crear un nuevo libro ---
    @app.route('/api/books', methods=['POST'])
    def create_book():
        # Obtenemos los datos del cuerpo de la petición (JSON)
        data = request.get_json()

        # Creamos el objeto Python
        new_book = Book(
            title=data.get('title'),
            author=data.get('author'),
            price=data.get('price')
        )

        # Añadimos a la sesión y hacemos commit (guardar en BD)
        session.add(new_book)
        session.commit()

        # Devolvemos el libro creado con código 201 (Created)
        return jsonify({
            'id': new_book.id,
            'title': new_book.title,
            'author': new_book.author,
            'price': new_book.price
        }), 201

    # --- UPDATE (PUT): Actualizar un libro ---
    @app.route('/api/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        data = request.get_json()
        book = session.query(Book).get(book_id)

        if book is None:
            return jsonify({"error": "Book Not Found"}), 404

        # Actualizamos los campos si vienen en el JSON
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'price' in data:
            book.price = data['price']

        session.commit()  # Guardamos cambios

        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price
        }), 200

    # --- DELETE: Eliminar un libro ---
    @app.route('/api/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = session.query(Book).get(book_id)

        if book is None:
            return jsonify({"error": "Book Not Found"}), 404

        session.delete(book)
        session.commit()

        return jsonify({"message": "Deleted successfully"}), 200