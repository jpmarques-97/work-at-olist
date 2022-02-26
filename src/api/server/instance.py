from flask import Flask
from flask_restx import Api
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

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
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db = SQLAlchemy(self.app)

    def run(self):
        self.app.run(
            debug=True
        )

server = Server()