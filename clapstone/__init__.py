from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from clapstone.config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_message_category = "info"
login_manager.login_view = "admins.login"


def create_app(config_class=Config):
    from .cli import (
        createadmin,
    )  # pylint: disable=import-outside-toplevel, import-error

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.app_context().push()

    migrate = Migrate(app, db, compare_type=True)  # pylint: disable=unused-variable

    from clapstone.admins.routes import admins
    from clapstone.main.routes import main
    from clapstone.jobOffers.routes import joboffer

    app.register_blueprint(admins)
    app.register_blueprint(main)
    app.register_blueprint(joboffer)

    app.cli.add_command(createadmin)

    return app
