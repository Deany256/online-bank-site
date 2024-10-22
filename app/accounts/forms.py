from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# Account Creation Form
class AccountForm(FlaskForm):
    account_type = SelectField(
        'Account Type', 
        choices=[('savings', 'Savings'), ('checking', 'Checking')], 
        validators=[DataRequired()]
    )
    initial_deposit = DecimalField(
        'Initial Deposit ($)', 
        validators=[DataRequired(), NumberRange(min=0.01, message="Must be greater than zero.")]
    )
    submit = SubmitField('Create Account')
