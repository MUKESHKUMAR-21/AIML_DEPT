from app import app, db
from models import SupportTicket

with app.app_context():
    # This will create the new support_ticket table without touching existing tables
    db.create_all()
    print("Database updated with SupportTicket table.")
