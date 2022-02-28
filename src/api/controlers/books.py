from flask_restx import reqparse, Resource
from datetime import datetime

from api.server.instance import server
from api.models.bookschema import bookSchema, authorSchema
from api.models.books import *

app, api = server.app, server.api
parser = reqparse.RequestParser()
parser.add_argument('title', required=False)
parser.add_argument('edition', required=False)
parser.add_argument('publication_year', required=False)
parser.add_argument('author_id', required=False)


@api.route('/books')
class BookList(Resource):

    @api.expect(parser)
    def get(self):
        book = Book.query
        args = parser.parse_args()
        if args['title']:
            book = book.filter_by(title=args['title'])
        if args['edition']:
            book = book.filter_by(edition=args['edition'])
        if args['publication_year']:
            book = book.filter_by(title=args['publication_year'])
        if args['author_id']:
            book = book.filter_by(title=args['author_id'])
        books = book.all()
        books = [{
                    "id": book.id,
                    "title": book.title,
                    "edition": book.edition,
                    "publication_year": book.publication_year.strftime('%Y-%m-%d'),
                    'authors': [{'name': author.name} for author in  book.authors]
                } for book in books]
        return books, 200

    @api.expect(bookSchema)
    def post(self):
        response = api.payload
        result = 'O livro nao foi inserido', 200
        authors_id = response['authors_id']
        if authors_id:
            book = Book(
                            title=response['title'], 
                            edition=response['edition'], 
                            publication_year=datetime.strptime(response['publication_year'],'%Y-%m-%d'),
                        )
            for author_id in authors_id:
                author = Author.query.filter_by(id=author_id).first()
                book.authors.append(author)
            server.db.session.add(book)
            server.db.session.commit()
            result = response, 200
            print(book.authors)
        return result

    

@api.route('/books/<int:id>')
class BookSingle(Resource):

    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        print(Book.query.filter_by(id=id).first())
        result = 'Book not found', 200
        if book:
            result = {
                'title': book.title,
                'edition': book.edition,
                'publication_year': book.publication_year.strftime('%Y-%m-%d'),
                'authors': [{'name': author.name} for author in  book.authors]
                }, 200
            
        return result
    
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        result = 'Book not found', 200
        print(book)
        if book:
            server.db.session.delete(book)
            server.db.session.commit()
            result = 'Book has been deleted', 200
        return result
    
    @api.expect(bookSchema)
    def put(self, id):
        response = api.payload
        book = Book.query.filter_by(id=id).first()
        result = 'Book not fount', 200
        if book:
            if 'title' in response.keys():
                book.title = response['title']
            if 'publication_year' in response.keys():
                book.publication_year = datetime.strptime(response['publication_year'],'%Y-%m-%d')
            if 'edition' in response.keys():
                book.edition = response['edition']
            if 'authors_id' in response.keys():
                book.authors = []
                for author_id in response['authors_id']:
                    author = Author.query.filter_by(id=author_id).first()
                    book.authors.append(author)
            server.db.session.commit()
            result = {
                    'title': book.title,
                    'edition': book.edition,
                    'publication_year': book.publication_year.strftime('%Y-%m-%d'),
                    'authors': [{'name': author.name} for author in  book.authors]
                    }, 200
        return result


@api.route('/authors')
class AuthorList(Resource):

    def get(self):
        authors = Author.query.all()
        authors = [{
                    "id" : author.id,
                    "name": author.name,
                    "books": [{"book_title": book.title} for book in author.books]
                    } for author in authors]
        return authors, 200

    @api.expect(authorSchema)
    def post(self):
        response = api.payload
        author = Author(name = response['name'])
        server.db.session.add(author)
        server.db.session.commit()
        return response, 200