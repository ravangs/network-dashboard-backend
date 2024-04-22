from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

def get_db():
    """
    Configuration method to return db instance
    """
    if 'mongo' not in g:
        g.mongo = PyMongo(current_app)
    
    return g.mongo.db

db = LocalProxy(get_db)
