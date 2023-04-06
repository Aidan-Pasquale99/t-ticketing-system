from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, HiddenField
from wtforms.validators import InputRequired


class CreateTicketForm(FlaskForm):
    name = StringField(
        "Ticket Name", 
        validators=[InputRequired()]
    )

    description = TextAreaField(
        "Ticket Description",
        validators=[InputRequired()]        
    )

    status = SelectField(u"Ticket Status", 
        default='',
        choices=[
            ("To Do"),
            ("In Progress"),
            ("Blocked"),
            ("Completed")
        ],
        validators=[InputRequired()]
        )

    department = SelectField(u"Department",
        default='',
        validators=[InputRequired()]
        )
    
    category = SelectField(u"Category",
        default='',
        validators=[InputRequired()]
        )
    
    due_date = DateField(
        "Due Date",
        validators=[InputRequired()]
        )
    
    updated_by = HiddenField("updated_by")

    updated_date = HiddenField("updated_date")