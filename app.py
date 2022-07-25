from flask import Flask
from configparser import ConfigParser

from repository.db import configure_db, configure_ma, db
from services.users import usr
from services.tubes import test_tube, root


def create_app():
    # Init app
    app = Flask(__name__)

    # Configure repository
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///repository/example.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    configure_db(app)
    configure_ma(app)

    # Init secret from config file
    config = ConfigParser()
    config.read("secret.config")
    app.secret_key = config['DEFAULT']["secret_key"]

    # blueprint for services
    app.register_blueprint(root, url_prefix='/')
    app.register_blueprint(usr, url_prefix='/user')
    app.register_blueprint(test_tube, url_prefix='/tube')

    return app


# Run Server
if __name__ == '__main__':
    api_app = create_app()
    api_app.run(debug=True)
