import click
from flask.cli import with_appcontext
import pandas as pd

from library.server.instance import server
from library.controlers.books import *

@click.command(name='import_authors')
@click.argument('csv')
@with_appcontext
def import_authors(csv):
    df = pd.read_csv(csv)
    df.to_sql('authors', con=server.engine, if_exists='replace')

server.app.cli.add_command(import_authors)

if __name__ == "__main__":
    server.run()