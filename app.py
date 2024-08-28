from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
    
db = SQLAlchemy()
api = Api()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    
    db.init_app(app)
    api.init_app(app)
    # 初始化 API
    from api import init_api
    init_api(api)

    migrate.init_app(app, db)
    
    return app

