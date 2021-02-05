from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, BooleanField, SelectField, StringField, PasswordField
from wtforms.validators import Length, InputRequired, ValidationError, NumberRange, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", 
               validators=[InputRequired(), Length(3,50)])
    password = PasswordField("Password",
               validators=[InputRequired(), Length(3,50)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", 
               validators=[InputRequired(), Length(3,50)])
    password   = PasswordField("Password",
               validators=[InputRequired(), Length(3,50), EqualTo('confirm', message='Passwords must match')])
    confirm   = PasswordField("Confirm password",
               validators=[InputRequired(), Length(3,50)])
    submit = SubmitField("Register")
