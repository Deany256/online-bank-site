from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange, ValidationError
from app.models import User

# User Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        # Check if the username is already in use
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')

    def validate_email(self, email):
        # Check if the email is already registered
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')


# Account Creation Form
class AccountForm(FlaskForm):
    account_type = SelectField('Account Type', choices=[('savings', 'Savings'), ('checking', 'Checking')], validators=[DataRequired()])
    initial_deposit = DecimalField('Initial Deposit ($)', validators=[DataRequired(), NumberRange(min=0.01, message="Must be greater than zero.")])
    submit = SubmitField('Create Account')


# Transaction Form (e.g., for withdrawals or deposits)
class TransactionForm(FlaskForm):
    transaction_type = SelectField('Transaction Type', choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], validators=[DataRequired()])
    amount = DecimalField('Amount ($)', validators=[DataRequired(), NumberRange(min=0.01, message="Amount must be greater than zero.")])
    submit = SubmitField('Submit Transaction')
