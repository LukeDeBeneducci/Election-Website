# IMPORTS #

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


# CONFIG #

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.account.views import account_blueprint

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(account_blueprint)

from .models import User

# Login Manager
login_manager.login_view ="users.home"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

