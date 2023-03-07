from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from models import Base, Author, Book
import mysql.connector

from schema import BookSchema, AuthorSchema
from custom_json_encoder import CustomJSONEncoder

app = Flask(__name__)
cors = CORS(app)
app.json_encoder = CustomJSONEncoder

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/test'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


@app.before_first_request
def setup():
    Base.metadata.create_all(db.engine)


@app.route('/books', methods=['GET'])
@cross_origin()
def get_books():
    books = db.session.query(Book).all()
    # methode without schema
    # return jsonify([book.__dict__ for book in books])
    # methode with schema
    #return books_schema.dumps(books)
    return  Book.serialize_list(books)

@app.route('/authors', methods=['GET'])
@cross_origin()
def get_authors():
    authors = db.session.query(Author).all()
    # methode without schema
    return Author.serialize_list(authors)
    # methode with schema
    # return jsonify(author_schema.dumps(authors))


@app.route('/author', methods=['POST'])
@cross_origin()
def create_author():
    data = request.json
    author = Author(name=data['name'])
    db.session.add(author)
    db.session.commit()
    pass
    # return Author.serialize(author)
    return author_schema.dumps(author)


@app.route('/books', methods=['POST'])
@cross_origin()
def create_book():
    data = request.json
    author = Author()
    if not ('author.id' in data):
        author = Author(name=data['author']['name'])
        db.session.add(author)
        db.session.commit()
    else:
        author = Author(id=data['author']['id'], name=data['author']['name'])

    book = Book(title=data['title'], author=author)
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dumps(book))


@app.route('/books', methods=['PUT'])
@cross_origin()
def update_book():
    data = request.json
    book = db.session.query(Book).filter_by(id=data['id']).first()
    book.title = data.get('title', book.title)
    author = db.session.query(Author).filter_by(id=data['author']['id'])
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    else:
        book.author_id = data['author']['id']

    if 'books' in author:
        author.books.append(book)
        db.session.commit()
        # author.books.clear()
    # db.session.commit()

    db.session.commit()
    return Book.serialize(book)


@app.route('/books/<int:book_id>', methods=['DELETE'])
@cross_origin()
def delete_book(book_id):
    book = db.session.query(Book).filter_by(id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return '', 204


@app.route('/book/<int:book_id>', methods=['GET'])
@cross_origin()
def get_book(book_id):
    book = db.session.query(Book).filter_by(id=book_id).first()
    if not book:
        return jsonify({'message': 'User not found'}), 404
    return book_schema.dumps(book)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
