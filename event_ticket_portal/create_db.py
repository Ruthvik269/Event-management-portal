# create_db.py
from event_ticket_portal.app import app, db
from event_ticket_portal.models import User, Event
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

with app.app_context():
    print("Dropping existing tables (if any)...")
    db.drop_all()
    print("Creating tables...")
    db.create_all()

    # --- Create Demo Users ---
    print("Adding demo users...")
    organizer = User(
        name="John Organizer",
        email="organizer@example.com",
        password=generate_password_hash("organizer123"),
        phone="9876543210",
        is_organizer=True
    )
    user = User(
        name="Alice Attendee",
        email="alice@example.com",
        password=generate_password_hash("user123"),
        phone="9123456780",
        is_organizer=False
    )

    db.session.add_all([organizer, user])
    db.session.commit()

    # --- Create Demo Events ---
    print("Adding demo events...")
    e1 = Event(
        organizer_name=organizer.name,
        title="Music Fest 2025",
        category="Concert",
        date=datetime.utcnow() + timedelta(days=5),
        venue="City Auditorium",
        total_seats=100,
        available_seats=100,
        ticket_price=500.00,
        description="A fun-filled evening with live music performances."
    )

    e2 = Event(
        organizer_name=organizer.name,
        title="Tech Conference",
        category="Technology",
        date=datetime.utcnow() + timedelta(days=10),
        venue="Tech Park Convention Hall",
        total_seats=150,
        available_seats=150,
        ticket_price=800.00,
        description="Explore the future of technology and innovation."
    )

    db.session.add_all([e1, e2])
    db.session.commit()
    print("Database setup complete with demo data ✅")
