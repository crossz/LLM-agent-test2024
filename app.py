from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
    
db = SQLAlchemy() ## this must be first, even the following import clause
api = Api()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    
    ## init db, api and migrate
    db.init_app(app)
    
    from api import init_api
    api.init_app(app)
    init_api(api)

    migrate.init_app(app, db)
    
    return app

