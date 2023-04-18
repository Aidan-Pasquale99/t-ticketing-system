from decouple import config
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app(config=None):
    from decouple import config
    
    app = Flask(__name__)
    app.config.from_object(config("APP_SETTINGS"))

    login_manager = LoginManager()
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db, render_as_batch=True)

    with app.app_context():
        
        from src.accounts.views import accounts_bp
        from src.core.views import core_bp
        from src.tickets.views import tickets_bp
    
        app.register_blueprint(accounts_bp)
        app.register_blueprint(core_bp)
        app.register_blueprint(tickets_bp)
    
        from src.accounts.models import User
    
        login_manager.login_view = "accounts.login"
    
    
        # create tables
        db.create_all()

        # create default admin user and my user if they do not exist
        admin_exists = db.session.query(User).filter_by(email="admin@t.com").first()
        if not admin_exists:
            admin_user = User(email="admin@t.com", password="tadmin", is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
        
        my_user_exists = db.session.query(User).filter_by(email="aidan@t.com").first()
        if not my_user_exists:
            my_user = User(email="aidan@t.com", password="aidanpasquale")
            db.session.add(my_user)
            db.session.commit()
        
        from src.tickets.models import Department, TaskType
        
        # check if departments exist, if not, add them
        departments_exist = Department.query.all()
        if not departments_exist:
            departments = [
                Department(name = "Sales"),
                Department(name = "Product"),
                Department(name = "HR"),
                Department(name = "IT"),
                Department(name = "Finance")
            ]
            db.session.bulk_save_objects(departments)
            db.session.commit()

        # check if task_types for the 'Category' field of the tickets exist, if not, add them
        task_types_exist = TaskType.query.all()
        if not task_types_exist:
            sales_department_id = Department.query.filter_by(name="Sales").first().id
            product_department_id = Department.query.filter_by(name="Product").first().id
            hr_department_id = Department.query.filter_by(name="HR").first().id
            it_department_id = Department.query.filter_by(name="IT").first().id
            finance_department_id = Department.query.filter_by(name="Finance").first().id
            
            task_types = [
                TaskType(name = "Sales - Client Engagements", department_id=sales_department_id),
                TaskType(name = "Sales - Creating Leads", department_id=sales_department_id),
                TaskType(name = "Sales - Executing Deals", department_id=sales_department_id),

                TaskType(name = "Product - Development - Coding", department_id=product_department_id),
                TaskType(name = "Product - Development - Designing", department_id=product_department_id),
                TaskType(name = "Product - Development - Testing", department_id=product_department_id),

                TaskType(name = "HR - Hiring - Creating Job Adverts", department_id=hr_department_id),
                TaskType(name = "HR - Hiring - Job Candidate Interviews", department_id=hr_department_id),
                TaskType(name = "HR - Internal - Disciplinary Meetings", department_id=hr_department_id),

                TaskType(name = "IT - Internal Systems Management", department_id=it_department_id),
                TaskType(name = "IT - Hardware Upgrades & Maintenance", department_id=it_department_id),
                TaskType(name = "IT - Security Analysis", department_id=it_department_id),

                TaskType(name = "Finance - Financial Reporting", department_id=finance_department_id),
                TaskType(name = "Finance - Payroll Updates", department_id=finance_department_id),
                TaskType(name = "Finance - Finance Meetings", department_id=finance_department_id)
            ]
            db.session.bulk_save_objects(task_types)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()
    
    return app