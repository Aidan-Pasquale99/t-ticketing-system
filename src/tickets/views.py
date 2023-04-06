from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from src.tickets.models import Ticket, Department, TaskType
from src.tickets.forms import CreateTicketForm
from src import db


tickets_bp = Blueprint("tickets", __name__)


# validate that the ticket type (category) matches the selected department
def valid_ticket_type(ticket_department, ticket_category):
    
    department = Department.query.filter_by(id=ticket_department).first()
    applicable_task_types = department.task_types

    for id in applicable_task_types:
        if ticket_category == id:
            return True
        else:
            False
    # if ticket_category in applicable_task_types:
    #     return True
    # else:
    #     return False


@tickets_bp.route("/all_tickets")
@login_required
def all_tickets():
    return render_template("tickets/index.html", tickets=Ticket.query.all())


@tickets_bp.route("/<int:ticket_id>")
@login_required
def get_ticket(ticket_id):
    
    # get the ticket by the provided id
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.department = Department.query.get(ticket.department).name
    ticket.category = TaskType.query.get(ticket.category).name

    # check if the ticket has been updated, if it has, the user and time of update will be displayed on the ticket page
    if ticket.updated_by is None:
        ticket_updated = False
        return render_template("tickets/ticket.html", ticket=ticket)
    else:
        ticket_updated = True
        updated_date = ticket.updated_date.strftime("%Y-%m-%d %H:%M:%S")
        return render_template("tickets/ticket.html", ticket=ticket, ticket_updated=ticket_updated, updated_date=updated_date)


def validate_task_department_pair(task_type_id, department_id):
    task_type = TaskType.query.filter_by(id=task_type_id.id).first()
    if not task_type:
        return False
    if task_type.department_id is not department_id:
        return False
    return True


# create a new ticket using a wtform
@tickets_bp.route("/create_ticket", methods=(["GET","POST"]))
@login_required
def create_ticket():
    form = CreateTicketForm()

    # task_type_id = request.form.get('task_type_id')
    # department_id = request.form.get('department_id')
    
    # Query the departments and their task types
    departments = Department.query.join(TaskType).all()

    # Populate the form SelectField choices
    form.department.choices = [(str(d.id), d.name) for d in departments]
    form.category.choices = [(str(tt.id), tt.name) for d in departments for tt in d.task_types]

    if form.validate_on_submit():

        task_type_id = db.session.query(TaskType).filter_by(id=form.data["category"]).first()
        department_id = db.session.query(Department).filter_by(id=form.data["department"]).first()

        if not validate_task_department_pair(task_type_id, department_id):
            flash("Ticket Category must belong to the selected Department", "danger")
            return render_template("tickets/create_ticket.html", form=form)
        
        # validate that the user-inputted due date is not prior to the current date, if it is, 
        # produce an error pop-up and remain on the create ticket page         
        elif form.due_date.data < datetime.now().date():
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
    # form = CreateTicketForm()

    # # Query the departments and their task types
    # departments = Department.query.join(TaskType).all()

    # # Populate the form SelectField choices
    # form.department.choices = [(str(d.id), d.name) for d in departments]
    # form.category.choices = [(str(tt.id), tt.name) for d in departments for tt in d.task_types]

    # if form.validate_on_submit():
    #     # validate that the user-inputted due date is not prior to the current date, if it is, 
    #     # produce an error pop-up and remain on the create ticket page
    #     if form.due_date.data < datetime.now().date():
    #         flash("Due Date cannot be prior to the current date", "danger")
    #         return render_template("tickets/create_ticket.html", form=form)
        
    #     department = Department.query.filter_by(id=form.department.data).first()
    #     applicable_task_types = department.task_types

    #     task_type = TaskType.query.filter_by(id=form.category.data).first()
    #     applicable_departments = task_type.departments

    #     category_id_int = int(form.data['category'])

    #     valid_category_department = []
        
    #     for task in applicable_task_types:
    #         task_department_id = task.department
    #         if category_id_int == task_department_id:
    #             valid_category_department = True
    #         else:
    #             valid_category_department = False

    #     if valid_category_department:
    #         ticket = Ticket(
    #         name=form.name.data,
    #         description=form.description.data,
    #         status=form.status.data,
    #         department=form.department.data,
    #         category=form.category.data,
    #         due_date=form.due_date.data,
    #         created_by = current_user.email
    #         )
    #         db.session.add(ticket)
    #         db.session.commit()
    #         return redirect(url_for("tickets.all_tickets"))
    #     else:
    #         flash("Ticket Category must belong to the selected Department", "danger")
            # return render_template("tickets/create_ticket.html", form=form)

        # if int(form.category.data) in applicable_task_types:
        #     ticket = Ticket(
        #     name=form.name.data,
        #     description=form.description.data,
        #     status=form.status.data,
        #     department=form.department.data,
        #     category=form.category.data,
        #     due_date=form.due_date.data,
        #     created_by = current_user.email
        #     )
        #     db.session.add(ticket)
        #     db.session.commit()
        #     return redirect(url_for("tickets.all_tickets"))       
        
        # if not valid_ticket_type:
        #     flash("Task Category field must belong to the Department", "danger")
        #     return render_template("tickets/create_ticket.html", form=form)

    return render_template("tickets/create_ticket.html", form=form)


# update ticket view
@tickets_bp.route("/update_ticket/<int:ticket_id>", methods=(["GET", "POST"]))
@login_required
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
@login_required
def delete_ticket(ticket_id):
    if request.method == "POST":
        Ticket.query.filter_by(id=ticket_id).delete()
        db.session.commit()
        flash("Ticket deleted successfully", "success")
        
    return redirect(url_for("tickets.all_tickets"))