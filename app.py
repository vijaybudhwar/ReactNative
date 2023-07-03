# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    publication_date = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'cover_image_url': self.cover_image_url,
            'price': self.price,
            'rating': self.rating,
            'genre': self.genre,
            'publication_date': self.publication_date
        }

# Sample book data
sample_books = [
    {
        'title': 'Book 1',
        'author': 'Author 1',
        'description': 'This is Book 1 description.',
        'cover_image_url': 'https://example.com/book1.jpg',
        'price': 19.99,
        'rating': 4.5,
        'genre': 'Fiction',
        'publication_date': '2022-01-01'
    },
    {
        'title': 'Book 2',
        'author': 'Author 2',
        'description': 'This is Book 2 description.',
        'cover_image_url': 'https://example.com/book2.jpg',
        'price': 12.99,
        'rating': 3.8,
        'genre': 'Science Fiction',
        'publication_date': '2021-08-15'
    },
    # Add more sample books here
]

# Endpoint to get all books
@app.route('/api/books', methods=['GET'])
def get_books():
    books = [book.to_dict() for book in Book.query.all()]
    return jsonify(books)

# Endpoint to search for books
@app.route('/api/books/search', methods=['GET'])
def search_books():
    keyword = request.args.get('q')
    if not keyword:
        return jsonify(error='Search keyword not provided'), 400

    books = Book.query.filter(
        (Book.title.ilike(f'%{keyword}%')) |
        (Book.author.ilike(f'%{keyword}%')) |
        (Book.genre.ilike(f'%{keyword}%'))
    ).all()

    if not books:
        return jsonify(error='No books found'), 404

    return jsonify([book.to_dict() for book in books])

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()

        # Add sample book data to the database
        for book_data in sample_books:
            book = Book(**book_data)
            db.session.add(book)
        db.session.commit()

    app.run(debug=True)
