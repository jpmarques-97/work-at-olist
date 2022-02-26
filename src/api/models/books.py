from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from api.server.instance import server

class Author(server.db.Model):
   __tablename__ = 'author'
   id = server.db.Column(server.db.Integer, primary_key = True)
   name = server.db.Column(server.db.String(120))

   def __init__(self, name):
      self.name = name

   def __repr__(self):
      return '<User %r>' % self.name

class Book(server.db.Model):
   __tablename__ = 'book'
   id = server.db.Column(server.db.Integer, primary_key = True)
   title = server.db.Column(server.db.String(120))
   edition = server.db.Column(server.db.Integer)
   publication_year = server.db.Column(server.db.String(120))
   author_id = server.db.Column(server.db.ForeignKey('author.id'))

   def __repr__(self):
      return '<User %r>' % self.title