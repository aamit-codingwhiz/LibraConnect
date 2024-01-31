# app.py

from flask import Flask, jsonify, request, send_file
from books_data import get_books, add_book, update_book, delete_book
from flask_cors import CORS
import os
import uuid


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = get_books()
    return jsonify(books)


@app.route('/api/books', methods=['POST'])
def add_new_book():
    file = request.files['file']
    saved_info = save_file(file)
    print(f"saved_info: {saved_info}")
    print(f"request: {request.form.get('title')}")

    book_info = {
        'title': request.form.get('title'),
        'author': request.form.get('author'),
        # Save the file path for future reference
        'file_path': saved_info['file_path']
    }

    added_book = add_book(book_info)
    return jsonify(added_book)


# Function to save the file and return the file path
def save_file(file):
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)

    # Generate a unique filename using UUID
    unique_filename = str(uuid.uuid4()) + '.pdf'

    # Save the file with the unique filename
    file_path = os.path.join(upload_dir, unique_filename)
    file.save(file_path)

    return {
        'filename': unique_filename,
        'file_size': os.path.getsize(file_path),  # Get the file size
        'file_path': file_path
    }



@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_existing_book(book_id):
    updated_data = request.get_json()
    updated_book = update_book(updated_data, book_id)

    if updated_book:
        return jsonify(updated_book)
    else:
        return jsonify({"error": "Book not found"}), 404



@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_existing_book(book_id):
    deleted_book = delete_book(book_id)

    if deleted_book:
        print(f'book {book_id} deleted')
        return jsonify(deleted_book)
    else:
        print(f'book {book_id} not fount')
        return jsonify({"error": "Book not found"}), 404


@app.route('/api/uploads')
def show_uploads():
    return os.listdir('uploads')


@app.route('/<path:file_path>')
def serve_pdf(file_path):
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    # app.run(debug=True, ssl_context='adhoc')
    app.run(debug=True)
