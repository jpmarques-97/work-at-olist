from pydoc import describe
from flask_restx import fields

from api.server.instance import server

bookSchema = server.api.model('Book', {
    'title': fields.String(),
    'edition': fields.Integer(),
    'publication_year': fields.Date(),
    'authors_id': fields.List(fields.Integer)
})

authorSchema = server.api.model('Author', {
    'name': fields.String()
})