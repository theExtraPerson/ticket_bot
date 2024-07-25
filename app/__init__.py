from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        # Add initial tickets if the table is empty
        if Ticket.query.count() == 0:
            tickets = [
                Ticket(event='concert', price=5000, available=10),
                Ticket(event='movie', price=1500, available=20),
                Ticket(event='theater', price=3000, available=5)
            ]
            db.session.bulk_save_objects(tickets)
            db.session.commit()
    
    # Define routes
    @app.route('/tickets', methods=['GET'])
    def get_tickets():
        tickets = Ticket.query.all()
        return jsonify([{ 'event': t.event, 'price': t.price, 'available': t.available } for t in tickets])

    @app.route('/purchase', methods=['POST'])
    def purchase_ticket():
        data = request.json
        event = data.get('event')
        payment_ref = data.get('payment_ref')

        ticket = Ticket.query.filter_by(event=event).first()
        if ticket and ticket.available > 0:
            payment_success = verify_payment(payment_ref)
            if payment_success:
                ticket.available -= 1
                db.session.commit()
                return jsonify({ 'message': f'Ticket for {event} purchased successfully.' }), 200
            else:
                return jsonify({ 'message': 'Payment verification failed.' }), 400
        else:
            return jsonify({ 'message': f'No tickets available for {event}.' }), 400

    return app

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)  # price in cents
    available = db.Column(db.Integer, nullable=False)

def verify_payment(payment_ref):
    # Replace with your MTN Open API payment verification logic
    url = f'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay/{payment_ref}'
    headers = {
        'Ocp-Apim-Subscription-Key': 'YOUR_SUBSCRIPTION_KEY',
        'X-Reference-Id': payment_ref,
        'X-Target-Environment': 'sandbox',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get('status')
        return status == 'SUCCESSFUL'
    return False
