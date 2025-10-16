from event_ticket_portal.app import app, db

if __name__ == '__main__':
    # Ensure database tables exist
    with app.app_context():
        db.create_all()
    # Start development server
    app.run(debug=True)
