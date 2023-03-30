from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, HiddenField
from wtforms.validators import InputRequired


class CreateTicketForm(FlaskForm):
    ticket_name = StringField(
        "Ticket Name", 
        validators=[InputRequired()]
    )

    ticket_description = TextAreaField(
        "Ticket Description"
    )

    status = SelectField(u'Ticket Status', choices=[
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('blocked', 'Blocked'),
        ('completed', 'Completed')
        ],
        validators=[InputRequired()]
        )

    department = SelectField(u'Department', choices=[
        ('product', 'Product'),
        ('it', 'IT'),
        ('sales', 'Sales'),
        ('hr', 'HR'),
        ('finance', 'Finance')
        ],
        validators=[InputRequired()]
        )
    
    # TODO: (nice to do) options should be restricted based on the department selected above
    # Would have to be department table with task types?
    category = SelectField(u'Category', choices=[
        ('Development - Coding'),
        ('Development - Testing'),
        ('Development - Documenting')
        ],
        validators=[InputRequired()]
        )
    
    due_date = DateField(
        'Due Date', 
        validators=[InputRequired()]
        )
    
    updated_by = HiddenField('updated_by')

    updated_date = HiddenField('updated_date')