from src.tickets.models import Ticket
from datetime import datetime


def test_new_ticket():
    """
    GIVEN a Ticket model
    WHEN a new Ticket is created
    THEN check the id, name, description, status, department, category, 
    due_date, created_by, updated_by, created_date, updated_date fields are defined correctly
    """

    ticket = Ticket(
        name = "Test ticket",
        description = "Test ticket description",
        status = "To Do",
        department = "Sales",
        category = "Sales - Executing Deals",
        due_date = datetime(2025, 5, 17),
        created_by= "aidan@t.com"
    )

    assert ticket.name == "Test ticket"
    assert ticket.description == "Test ticket description"
    assert ticket.status == "To Do"
    assert ticket.department == "Sales"
    assert ticket.category == "Sales - Executing Deals"
    assert ticket.due_date == datetime(2025, 5, 17)
    assert ticket.created_by == "aidan@t.com"