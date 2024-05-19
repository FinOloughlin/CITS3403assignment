from flask import Flask
from app.config import Config, DeploymentConfig, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)
    from app.blueprints import main
    flaskApp.register_blueprint(main)
    db.init_app(flaskApp)

    return flaskApp

from app import models