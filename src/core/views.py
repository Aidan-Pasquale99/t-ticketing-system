from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func

from src.tickets.models import Ticket
from src import db

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
@login_required
def home():
    # get number of tickets
    number_of_tickets = db.session.query(func.count(Ticket.id)).scalar()
    if number_of_tickets > 0:
        # if tickets are present in the database, count the number of tickets in each possible status
        to_do_tickets = db.session.query(func.count(Ticket.status)).filter(Ticket.status == "to-do").scalar()
        in_prog_tickets = db.session.query(func.count(Ticket.status)).filter(Ticket.status == "in-progress").scalar()
        blocked_tickets = db.session.query(func.count(Ticket.status)).filter(Ticket.status == "blocked").scalar()
        completed_tickets = db.session.query(func.count(Ticket.status)).filter(Ticket.status == "completed").scalar()
        tickets_exist = True
        # render home page template, pass in number of tickets in each status to be displayed on the graph
        return render_template("core/index.html", tickets_exist=tickets_exist, to_do_tickets=to_do_tickets, in_prog_tickets=in_prog_tickets, blocked_tickets=blocked_tickets, completed_tickets=completed_tickets)
    # if no tickets are present in the database, render the home page without the chart labels and no chart
    else:
        tickets_exist = False
        return render_template("core/index.html", tickets_exist=tickets_exist)