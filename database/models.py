from .db import db


# User Class/Model
class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String, unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    tubes = db.relationship('Tube', backref='person', lazy=True)

    def __init__(self, email, id=None) -> None:
        self.id = id
        self.email = email

    def __repr__(self):
        return f'<User ID: {self.id}, Email: {self.email}>'


# Tube Class/Model
class Tube(db.Model):
    __tablename__ = 'tube'
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __init__(self, barcode, status, user_id, id=None) -> None:
        self.id = id
        self.barcode = barcode
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return f'<Tube ID: {self.id}, Barcode: {self.barcode}, Status: {self.status} User ID: {self.user_id}>'

