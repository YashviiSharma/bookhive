from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Books Table
class Book(db.Model):
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    publisher = db.Column(db.String(255), nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    total_copies = db.Column(db.Integer, default=1, nullable=False)
    available_copies = db.Column(db.Integer, default=1, nullable=False)
    added_on = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Members Table
class Member(db.Model):
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=True)
    membership_date = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    membership_type = db.Column(db.Enum('Standard', 'Premium', name='membership_type_enum'), default='Standard', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    fine_due = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    last_updated = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# Transactions Table
class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id', ondelete='CASCADE'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    issue_date = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)
    due_date = db.Column(db.TIMESTAMP, nullable=False)
    return_date = db.Column(db.TIMESTAMP, nullable=True)
    fine_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    payment_status = db.Column(db.Enum('Paid', 'Pending', name='payment_status_enum'), default='Pending', nullable=False)
    status = db.Column(db.Enum('Issued', 'Returned', 'Overdue', name='status_enum'), default='Issued', nullable=False)

    # Relationships
    book = db.relationship('Book', backref=db.backref('transactions', lazy=True, cascade='all, delete'))
    member = db.relationship('Member', backref=db.backref('transactions', lazy=True, cascade='all, delete'))
