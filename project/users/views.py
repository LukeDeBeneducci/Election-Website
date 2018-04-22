# IMPORTS #
from flask import render_template, request, url_for, redirect, session, flash, Blueprint
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from project import db
from project.models import User, bcrypt, Details

# CONFIG #
users_blueprint = Blueprint('users', __name__, template_folder='templates')

## ROUTES ##
db.create_all()
db.session.commit()

# Home Page: contains the user loging form, compares entered details to the database.
# Correct login will redirect to account page.
@users_blueprint.route('/', methods=['GET', 'POST'])
def home():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash("You were just logged in!")
                return redirect(url_for('account.account'))
            else:
                error = "Invalid credentials. Please try again."
    return render_template("index.html", form=form, error=error)

# Registration Page: contains the registration form which will insert entered details
# into the database -> password is hashed on entry. Correct registration will redirect to account page.
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        if form.validate_on_submit():
            details = Details(
                city=form.city.data,
                age=form.age.data,
                last=form.lastname.data,
                first=form.firstname.data
            )
            db.session.add(details)
            user = User(
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You were just logged in!")
            return redirect(url_for('account.account'))
        else:
            error = "Submission Failed"
            return render_template("register.html", form=form, error=error)
    return render_template("register.html", form=form, error=error)

# Logout Page: If user is logged in -> @login_required -> user will be logged out and redirected to home page.
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were just logged out")
    return redirect(url_for('users.home'))

