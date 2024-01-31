# books_data.py

import json
import os

JSON_FILE_PATH = 'books.json'


def get_books():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)


def add_book(new_book):
    books = get_books()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    _write_to_json(books)
    return new_book


def update_book(updated_data, book_id):
    books = get_books()
    for book in books:
        if book['id'] == book_id:
            book.update(updated_data)
            _write_to_json(books)
            return book
    return None


def delete_book(book_id):
    books = get_books()
    for i, book in enumerate(books):
        if book['id'] == book_id:
            deleted_book = books.pop(i)
            if os.path.exists(deleted_book['file_path']):
                os.remove(deleted_book['file_path'])
            _write_to_json(books)
            return deleted_book
    return None


def _write_to_json(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=2)
