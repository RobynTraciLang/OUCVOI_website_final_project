from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_app.controllers import member_controller, suggestion_controller, donation_controller, faq_controller, event_controller, legal_controller, shop_controller, contact_controller, director_controller


if __name__=='__main__':
    app.run(debug=True)