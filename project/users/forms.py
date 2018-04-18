from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Login Form -> username is email / password
class LoginForm(FlaskForm):
    username = StringField('email', validators=[Email(), DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

# Registration Form -> first name / last name / city / age / email / password / password confirmation
class RegisterForm(FlaskForm):
    firstname = StringField(
        'firstname',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    lastname = StringField(
        'lastname',
        validators=[DataRequired(), Length(min=2, max=25)]
    )
    city = StringField(
        'city',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    age = IntegerField(
        'age',
        validators=[DataRequired()]
    )
    email = StringField(
        'email',
        validators=[DataRequired(), Email(), Length(max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=12)]
    )
    repeatpassword = PasswordField(
        'repeatpassword',
        validators=[DataRequired(), EqualTo('password', message="Passwords must match.")]
    )

