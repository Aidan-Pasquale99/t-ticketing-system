from src import db
from sqlalchemy import func

# TODO: (maybe) rename class to Ticket, and add __tablename__ = "tickets"
class tickets(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    ticket_name = db.Column(db.String(150))
    ticket_description = db.Column(db.Text)
    status = db.Column(db.String(50))
    department = db.Column(db.String(50))
    category = db.Column(db.String(50))
    created_by = db.Column(db.ForeignKey('users.email'))
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, ticket_name, ticket_description, status, department, category, created_by, created_date=func.now()):
        self.ticket_name = ticket_name
        self.ticket_description = ticket_description
        self.status = status
        self.department = department
        self.category = category
        self.created_by = created_by
        self.created_date = created_date