from api.server.instance import server


book_authors = server.db.Table('book_authors',
   server.db.Column('book_id', server.db.Integer,  server.db.ForeignKey('book.id')),
   server.db.Column('user_id', server.db.Integer, server.db.ForeignKey('author.id')),
)

class Author(server.db.Model):
   __tablename__ = 'author'
   id = server.db.Column(server.db.Integer, primary_key = True)
   name = server.db.Column(server.db.String(120))
   books = server.db.relationship('Book', secondary=book_authors, backref='books')

   def __repr__(self):
      return f'<User {self.name}>'

class Book(server.db.Model):
   __tablename__ = 'book'
   id = server.db.Column(server.db.Integer, primary_key = True)
   title = server.db.Column(server.db.String(120))
   edition = server.db.Column(server.db.Integer)
   publication_year = server.db.Column(server.db.DateTime)
   authors = server.db.relationship('Author', secondary=book_authors, backref='authors')

   def __repr__(self):
      return f'<Book {self.title}>'