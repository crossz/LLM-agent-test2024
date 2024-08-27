from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    with app.app_context():
        db.create_all()

    # 初始化 API
    from .api import init_api
    init_api(api)

    return app
