import os
import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from flask import Flask, request
from .models import Ticket
from .services import verify_payment
from . import db

# Load the BOT_TOKEN from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN provided. Please set the BOT_TOKEN environment variable.")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
application = Application.builder().token(BOT_TOKEN).build()

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to the Ticket Bot! Use /buy to purchase tickets.')

def buy(update: Update, context: CallbackContext):
    tickets = Ticket.query.all()
    buttons = [[InlineKeyboardButton(ticket.event, callback_data=ticket.event)] for ticket in tickets]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text('Select an event:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    event = query.data
    ticket = Ticket.query.filter_by(event=event).first()
    if ticket and ticket.available > 0:
        # Assuming a payment reference is obtained here
        payment_ref = 'mock_payment_ref'
        payment_success = verify_payment(payment_ref)
        if payment_success:
            ticket.available -= 1
            db.session.commit()
            query.edit_message_text(f'Ticket for {event} purchased successfully.')
        else:
            query.edit_message_text('Payment verification failed.')
    else:
        query.edit_message_text(f'No tickets available for {event}.')

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('buy', buy))
application.add_handler(CallbackQueryHandler(button))

def run_bot():
    application.run_polling()

if __name__ == '__main__':
    run_bot()
