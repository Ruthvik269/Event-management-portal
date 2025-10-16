from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DecimalField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    phone = StringField('Phone')
    is_organizer = BooleanField('Register as Organizer?')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category')
    date = DateTimeField('Date (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    total_seats = IntegerField('Total Seats', validators=[DataRequired(), NumberRange(min=1)])
    ticket_price = DecimalField('Ticket Price', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Event')
