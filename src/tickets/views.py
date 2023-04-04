from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from src.tickets.models import Ticket
from src.tickets.forms import CreateTicketForm
from src import db


tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/all_tickets")
@login_required
def all_tickets():
    return render_template("tickets/index.html", tickets=Ticket.query.all())


@tickets_bp.route("/<int:ticket_id>")
def get_ticket(ticket_id):
    ticket = ticket=Ticket.query.filter_by(id=ticket_id).first()
    # check if the ticket has been updated, if it has, the user and time of update will be displayed on the ticket page
    if ticket.updated_by is None:
        ticket_updated = False
        return render_template("tickets/ticket.html", ticket=ticket)
    else:
        ticket_updated = True
        updated_date = ticket.updated_date.strftime("%Y-%m-%d %H:%M:%S")
        return render_template("tickets/ticket.html", ticket=ticket, ticket_updated=ticket_updated, updated_date=updated_date)


# create a new ticket using a wtform
@tickets_bp.route("/create_ticket", methods=(["GET","POST"]))
def create_ticket():
    form = CreateTicketForm()
    if form.validate_on_submit():
        # validate theat the user-inputted due date is not prior to the current date, if it is, 
        # produce an error pop-up and remain on the create ticket page
        if form.due_date.data < datetime.now().date():
            flash("Due Date cannot be prior to the current date", "danger")
            return render_template("tickets/create_ticket.html", form=form)
        else:
            ticket = Ticket(
                name=form.name.data,
                description=form.description.data,
                status=form.status.data,
                department=form.department.data,
                category=form.category.data,
                due_date=form.due_date.data,
                created_by = current_user.email
                )
            db.session.add(ticket)
            db.session.commit()

        return redirect(url_for("tickets.all_tickets"))
    return render_template("tickets/create_ticket.html", form=form)


# update ticket view
@tickets_bp.route("/update_ticket/<int:ticket_id>", methods=(["GET", "POST"]))
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.updated_by = current_user.email
    ticket.updated_date = datetime.utcnow()
    form = CreateTicketForm(obj=ticket)

    # if update form is submitted, update the ticket
    if request.method == "POST" and form.validate():
        if form.validate_on_submit():            
            form.populate_obj(ticket)
            db.session.commit()
        return redirect(url_for("tickets.get_ticket", ticket_id=ticket_id))

    # if the update page is called via the update button, show the update page with the fields 
    # populated with current ticket data
    return render_template("tickets/update_ticket.html", ticket=ticket, form=form)


# delete ticket view, accessed via the delete button which is only available in the UI for admin users
@tickets_bp.route("/delete_ticket/<int:ticket_id>", methods=(["POST"]))
def delete_ticket(ticket_id):
    if request.method == "POST":
        Ticket.query.filter_by(id=ticket_id).delete()
        db.session.commit()
        flash("Ticket deleted successfully", "success")
        
    return redirect(url_for("tickets.all_tickets"))