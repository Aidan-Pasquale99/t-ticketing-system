from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from src.tickets.models import tickets
from src import db


tickets_bp = Blueprint("tickets", __name__)


@tickets_bp.route("/all_tickets")
@login_required
def all_tickets():
    return render_template("tickets/index.html", tickets=tickets.query.all())

def get_ticket(ticket_id):
    ticket=tickets.query.filter_by(id=ticket_id).first()
    # ('SELECT * FROM tickets WHERE id = ?',(ticket_id,)).fetchone()
    if ticket is None:
        flash("Ticket not found", "error")
        abort(404)
    return ticket

@tickets_bp.route('/<int:ticket_id>')
def get_ticket(ticket_id):
    # ticket = get_ticket(ticket_id=ticket_id)
    ticket = ticket=tickets.query.filter_by(id=ticket_id).first()
    return render_template('tickets/ticket.html', ticket=ticket)

@tickets_bp.route("/create_ticket", methods=(['GET','POST']))
@login_required
def create_ticket():
    if request.method == 'POST':
        if not all([
            request.form['ticket-name'],
            request.form['ticket-description'],
            # TODO: Get due date input working
            # request.form['due-date'],
            request.form['ticket-status'],
            request.form['department'],
            request.form['category']
            ]):
            flash('Please enter all the fields', 'error')
        else:
            # due_date = datetime.strptime(request.form['due-date'], '%Y-%m-%d')
            ticket = tickets(
                ticket_name = request.form['ticket-name'],
                ticket_description = request.form['ticket-description'],
                # TODO: Get due date input working
                # due_date = request.form['due-date'],
                status = request.form['ticket-status'],
                department = request.form['department'],
                category = request.form['category'],
                created_by = current_user.email
            )

            db.session.add(ticket)
            db.session.commit()

            flash('Ticket created', "info")

            return redirect(url_for('tickets.all_tickets'))
    return render_template("tickets/create_ticket.html")

# update ticket view
@tickets_bp.route("/update_ticket/<int:ticket_id>", methods=(['GET', 'POST']))
def update_ticket(ticket_id):
    if request.method == 'POST':
        ticket = get_ticket(ticket_id=ticket_id)
        
        form = ItemForm(obj=item)
        
        db.session.commit()
        flash("Ticket updated successfully", "success")

        return redirect(url_for('tickets.all_tickets'))
    return render_template("tickets/create_ticket.html")

# delete ticket view, accessed via the delete button which is only available in the UI for admin users
@tickets_bp.route("/delete_ticket/<int:ticket_id>", methods=(['POST']))
def delete_ticket(ticket_id):
    if request.method == 'POST':
        tickets.query.filter_by(id=ticket_id).delete()
        db.session.commit()
        flash("Ticket " + str(ticket_id) + " deleted successfully", "success")
    
    return redirect(url_for('tickets.all_tickets'))
