from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config['MONGO_URI'] = os.environ.get('DATABASE_URL')
    app.config['DEBUG'] = True
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    mongo = PyMongo(app)
    api = Api(app)

    from network_dashboard.api.devices import devices_api
    CORS(devices_api)
    app.register_blueprint(devices_api)

    return app
