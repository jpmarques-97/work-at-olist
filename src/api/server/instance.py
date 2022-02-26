from flask import Flask
from flask_restx import Api
from sqlalchemy import create_engine

class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            version='0.1.0',
            title='Sample Book Api',
            description='A simple book API',
            doc='/docs'
            )
        self.engine = create_engine('sqlite:///test.db')

    def run(self):
        self.app.run(
            debug=True
        )

server = Server()