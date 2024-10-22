from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

# User Model
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

    # Set the password (hashing for security)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verify the password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Account Model
class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(64), nullable=False)  # e.g., 'Savings', 'Checking'
    balance = db.Column(db.Float, default=0.0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def deposit(self, amount):
        """Deposit money into the account."""
        self.balance += amount

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if self.balance >= amount:
            self.balance -= amount
        else:
            raise ValueError("Insufficient balance")

    def __repr__(self):
        return f'<Account {self.account_type} (Balance: {self.balance})>'

# Transaction Model
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(64), nullable=False)  # e.g., 'Deposit', 'Withdrawal'
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)

    def __repr__(self):
        return f'<Transaction {self.transaction_type} of {self.amount} on {self.timestamp}>'
