from flask import Flask
from flask_restx import Api, Resource

from library.server.instance import server
from library.models.books import bookSchema, authorSchema

app, api = server.app, server.api

try:
    authors = [author[1] for author in server.engine.execute("SELECT * FROM authors").fetchall()]
except:
    authors = []

books = []


@api.route('/books')
class BookList(Resource):

    #@api.marshal_list_with(bookSchema)
    def get(self):
        return books, 200

    @api.expect(bookSchema)
    def post(self):
        response = api.payload
        author = authors[response['author_id']]
        response['author'] = author
        del response['author_id']
        books.append(response)
        return response, 200

@api.route('/authors')
class AuthorList(Resource):

    #@api.marshal_list_with(authorSchema)
    def get(self):
        return authors, 200

    @api.expect(authorSchema)
    def post(self):
        response = api.payload
        authors.append(response['name'])
        return response, 200