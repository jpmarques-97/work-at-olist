import click
from flask.cli import with_appcontext
import pandas as pd

from api.server.instance import server
from api.controlers.books import *
from api.models.books import *


@click.command(name='import_authors')
@click.argument('csv')
@with_appcontext
def import_authors(csv):
    df = pd.read_csv(csv)
    df.to_sql('author', con=server.db.engine, if_exists='append', index=False)

@click.command(name='create_db')
@with_appcontext
def create_db():
    server.db.create_all()

server.app.cli.add_command(import_authors)
server.app.cli.add_command(create_db)

if __name__ == "__main__":
    server.run()