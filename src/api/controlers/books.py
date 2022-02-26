from flask_restx import Api, Resource

from api.server.instance import server
from api.models.bookschema import bookSchema, authorSchema
from api.models.books import *

app, api = server.app, server.api


books = []


@api.route('/books')
class BookList(Resource):

    #@api.marshal_list_with(bookSchema)
    def get(self):
        books = Book.query.all()
        books = [{
                    "title": book.title,
                    "edition": book.edition,
                    "publication_year": book.publication_year,
                    "author_id": book.author_id
                } for book in books]
        return books, 200

    @api.expect(bookSchema)
    def post(self):
        response = api.payload
        author = Author.query.filter_by(id=response['author_id']).first()
        if author:
            book = Book(title=response['title'], edition=response['edition'], 
                        publication_year=response['publication_year'],
                        author_id = author.id)
            server.db.session.add(book)
            server.db.session.commit()
            return response, 200
        else:
            return 'author does not exist', 203

@api.route('/authors')
class AuthorList(Resource):

    #@api.marshal_list_with(authorSchema)
    def get(self):
        authors = Author.query.all()
        authors = [author.name for author in authors]
        return authors, 200

    @api.expect(authorSchema)
    def post(self):
        response = api.payload
        author = Author(response['name'])
        server.db.session.add(author)
        server.db.session.commit()
        return response, 200