from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()


def configure_ma(app):
    ma.init_app(app)


def configure_db(app):
    db.init_app(app)
    app.db = db
