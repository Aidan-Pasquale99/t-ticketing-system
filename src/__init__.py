from decouple import config
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from src.accounts.views import accounts_bp
from src.core.views import core_bp
from src.tickets.views import tickets_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)
app.register_blueprint(tickets_bp)

from src.accounts.models import User

login_manager.login_view = "accounts.login"

# create default admin user and my user
with app.app_context():
    db.create_all()
    admin_exists = db.session.query(User).filter_by(email="admin@temenos.com").first()
    if not admin_exists:
        admin_user = User(email="admin@temenos.com", password="temenosadmin", is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
    
    my_user_exists = db.session.query(User).filter_by(email="aidan@temenos.com").first()
    if not my_user_exists:
        my_user = User(email="aidan@temenos.com", password="aidanpasquale")
        db.session.add(my_user)
        db.session.commit()    

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()