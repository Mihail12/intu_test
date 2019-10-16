import os
from flask import Flask
from sqlalchemy_utils import database_exists, create_database

from models import db, CategoryType
from schemas import ma


user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'


def add_categories_to_db():
    category_types = ["jewellery", "florist", "hairdresser", "newsagent", "chemist", "butcher", "baker", "shoe shop",
                      "music shop", "others"]
    for type_name in category_types:
        db.session.add(CategoryType(name=type_name))
    db.session.commit()


def create_app():
    flask_app = Flask(__name__)
    flask_app.debug = True
    flask_app.secret_key = 'development'
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.app_context().push()
    db.init_app(flask_app)
    ma.init_app(flask_app)
    if not database_exists(DATABASE_CONNECTION_URI):
        print('Creating database.')
        create_database(DATABASE_CONNECTION_URI)
        db.create_all()
        add_categories_to_db()
    else:
        db.create_all()
    return flask_app
