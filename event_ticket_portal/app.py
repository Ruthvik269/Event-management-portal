from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from event_ticket_portal.config import Config
from event_ticket_portal.models import db, User, Event, Booking
from event_ticket_portal.forms import RegisterForm, LoginForm, EventForm

import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Point templates and static folder to the project's top-level templates and css directories
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'css')
app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ensure tables exist when starting the app. Using Flask's
# `before_first_request` decorator isn't available in this
# environment, so create tables explicitly before running.

@app.route('/')
def index():
    events = Event.query.filter(Event.date >= datetime.utcnow()).order_by(Event.date).all()
    return render_template('index.html', events=events)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hashed,
                    phone=form.phone.data, is_organizer=form.is_organizer.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app.route('/organizer/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_organizer:
        flash('Only organizers can create events.', 'danger')
        return redirect(url_for('index'))
    form = EventForm()
    if form.validate_on_submit():
        ev = Event(
            organizer_name=current_user.name,
            title=form.title.data,
            category=form.category.data,
            date=form.date.data,
            venue=form.venue.data,
            total_seats=form.total_seats.data,
            available_seats=form.total_seats.data,
            ticket_price=float(form.ticket_price.data),
            description=form.description.data
        )
        db.session.add(ev)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('index'))
    return render_template('organizer_create_event.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_organizer:
        events = Event.query.filter_by(organizer_name=current_user.name).all()
        return render_template('dashboard.html', events=events, organizer=True)
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', bookings=bookings, organizer=False)

@app.route('/book/<int:event_id>', methods=['POST'])
@login_required
def book(event_id):
    event = Event.query.get_or_404(event_id)
    qty = int(request.form['quantity'])
    if qty > event.available_seats:
        flash('Not enough seats available', 'danger')
        return redirect(url_for('event_detail', event_id=event_id))
    event.available_seats -= qty
    booking = Booking(user_id=current_user.id, event_id=event.id, quantity=qty)
    db.session.add(booking)
    db.session.commit()
    flash('Booking confirmed!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
