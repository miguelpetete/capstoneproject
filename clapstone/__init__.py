from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from clapstone.config import Config
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate = Migrate(app, db, compare_type=True)  # pylint: disable=unused-variable

    from clapstone.routes import routes
    from clapstone.admins.routes import admins
    from clapstone.main.routes import main

    app.register_blueprint(routes)
    app.register_blueprint(admins)
    app.register_blueprint(main)

    return app
