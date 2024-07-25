from flask import current_app as app
from flask import render_template
from flask import Blueprint, request, jsonify
from .models import Ticket
from .services import verify_payment
from .telegram_bot import bot
from . import db

bp = Blueprint('routes', __name__)

@bp.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([{ 'event': t.event, 'price': t.price, 'available': t.available } for t in tickets])

@bp.route('/purchase', methods=['POST'])
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

# Register the blueprint in the app
def init_app(app):
    app.register_blueprint(bp)