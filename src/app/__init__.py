import os
import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from src.app.config import app_config
from src.app.models.user import create_collection_user
from src.app.utils import mongo

app = Flask(__name__)
app.config.from_object(app_config[os.getenv("FLASK_ENV")])
mongo.init_app(app)
mongo_client = mongo.cx.get_database("users")

@click.command(name="create_collections")
@with_appcontext
def create_collections():
    create_collection_user(mongo_client)

@click.command(name="list_collections_users")
@with_appcontext
def list_collections_for_users():
    mongo_db = mongo.cx.get_database("users")
    print(mongo_db.list_collection_names())

@click.command(name="list_database")
@with_appcontext
def list_all_database():
    mongo_db = mongo.cx.list_database_names()
    print(mongo_db)

app.cli.add_command(create_collections)
app.cli.add_command(list_collections_for_users)
app.cli.add_command(list_all_database)

CORS(app)
