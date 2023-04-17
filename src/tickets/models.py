from src import db
from sqlalchemy import func


class Ticket(db.Model):

    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.ForeignKey("users.email"), nullable=False)
    updated_by = db.Column(db.ForeignKey("users.email"))
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_date = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, name, description, status, department, category, due_date, created_by, created_date=func.now()):
        self.name = name
        self.description = description
        self.status = status
        self.department = department
        self.category = category
        self.due_date = due_date
        self.created_by = created_by
        self.created_date = created_date

class Department(db.Model):

    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)

class TaskType(db.Model):

    __tablename__ = "task_types"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)

    # define the relationship with Department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    department = db.relationship('Department', backref='task_types')