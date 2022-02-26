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
                    "author_id": book.author_id
                } for book in books]
        return books, 200

    @api.expect(bookSchema)
    def post(self):
        response = api.payload
        author = Author.query.filter_by(id=response['author_id']).first()
        if author:
            book = Book(title=response['title'], edition=response['edition'], 
                        publication_year=datetime.strptime(response['publication_year'],'%Y-%m-%d'),
                        author_id = author.id)
            server.db.session.add(book)
            server.db.session.commit()
            return response, 200
        else:
            return 'author does not exist', 200
    

@api.route('/books/<int:id>')
class BookSingle(Resource):

    @api.marshal_with(bookSchema)
    def get(self, id):
        book = Book.query.filter_by(id=id).first()
        print(Book.query.filter_by(id=id).first())
        result = 'Book not found', 200
        if book:
            result = {
                'title': book.title,
                'edition': book.edition,
                'publication_year': book.publication_year.strftime('%Y-%m-%d'),
                'author_id': book.author_id
                }, 200
            
        return result
    
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        result = 'Book not found', 200
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
            if 'author_id' in response.keys():
                author = Author.query.filter_by(id=response['author_id']).first()
                book.author_id = author.id
            if 'title' in response.keys():
                book.title = response['title']
            if 'publication_year' in response.keys():
                book.publication_year = datetime.strptime(response['publication_year'],'%Y-%m-%d')
            if 'edition' in response.keys():
                book.edition = response['edition']
            server.db.session.commit()
            result = {
                    'title': book.title,
                    'edition': book.edition,
                    'publication_year': book.publication_year.strftime('%Y-%m-%d'),
                    'author_id': book.author_id
                    }, 200
        return result


@api.route('/authors')
class AuthorList(Resource):

    @api.marshal_list_with(authorSchema)
    def get(self):
        authors = Author.query.all()
        authors = [{"name": author.name} for author in authors]
        return authors, 200

    @api.expect(authorSchema)
    def post(self):
        response = api.payload
        author = Author(response['name'])
        server.db.session.add(author)
        server.db.session.commit()
        return response, 200