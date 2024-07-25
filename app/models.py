from . import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # price in cents
    available = db.Column(db.Integer, nullable=False)