from src import db
from sqlalchemy import func

# TODO: (nice to do) rename class to Ticket, and add __tablename__ = "tickets"
class tickets(db.Model):
    # TODO: (nice to do) clean up fields, remove ticket_ from all ideally
    id = db.Column(db.Integer, primary_key = True)
    ticket_name = db.Column(db.String(150))
    ticket_description = db.Column(db.Text)
    status = db.Column(db.String(50))
    department = db.Column(db.String(50))
    category = db.Column(db.String(50))
    due_date = db.Column(db.Date)
    created_by = db.Column(db.ForeignKey('users.email'))
    updated_by = db.Column(db.ForeignKey('users.email'))
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, ticket_name, ticket_description, status, department, category, due_date, created_by, created_date=func.now()):
        self.ticket_name = ticket_name
        self.ticket_description = ticket_description
        self.status = status
        self.department = department
        self.category = category
        self.due_date = due_date
        self.created_by = created_by
        self.created_date = created_date