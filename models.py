
import os
from peewee import Model, PostgresqlDatabase, CharField, IntegerField, TextField, BooleanField, DecimalField, AutoField, ForeignKeyField, DateTimeField, Check
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE = {
    'name': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT'))
}

db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port']
)

class BaseModel(Model):
    class Meta:
        database = db

# Books Table
class Book(BaseModel):
    book_id = AutoField(primary_key=True)
    title = CharField(max_length=255, null=False)
    author = CharField(max_length=255, null=False)
    isbn = CharField(max_length=20, unique=True, null=True)
    publisher = CharField(max_length=255, null=True)
    page_count = IntegerField(null=True)
    category = CharField(max_length=100, null=True)
    total_copies = IntegerField(default=1, null=False)
    available_copies = IntegerField(default=1, null=False)
    added_on = DateTimeField(default=datetime.utcnow, null=False)
    updated_on = DateTimeField(default=datetime.utcnow, null=False)
    rating = IntegerField(null=False, constraints=[Check('rating BETWEEN 1 AND 5')])  
    image_url = CharField(null=True)  

# Members Table
class Member(BaseModel):
    member_id = AutoField(primary_key=True)
    first_name = CharField(max_length=100, null=False)
    last_name = CharField(max_length=100, null=False)
    email = CharField(max_length=255, unique=True, null=False)
    phone = CharField(max_length=15, unique=True, null=False)
    address = TextField(null=True)
    membership_date = DateTimeField(default=datetime.utcnow, null=False)
    membership_type = CharField(choices=[('Standard', 'Standard'), ('Premium', 'Premium')], default='Standard', null=True)
    is_active = BooleanField(default=True, null=True)
    fine_due = DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True)
    last_updated = DateTimeField(default=datetime.utcnow, null=True)

# Transactions Table
class Transaction(BaseModel):
    transaction_id = AutoField(primary_key=True)
    book_id = ForeignKeyField(Book, backref='transactions', on_delete='CASCADE')
    member_id = ForeignKeyField(Member, backref='transactions', on_delete='CASCADE')
    issue_date = DateTimeField(default=datetime.utcnow, null=False)
    due_date = DateTimeField(null=False)
    return_date = DateTimeField(null=True)
    fine_amount = DecimalField(max_digits=10, decimal_places=2, default=0.00, null=False)
    payment_status = CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', null=False)
    status = CharField(choices=[('Issued', 'Issued'), ('Returned', 'Returned'), ('Overdue', 'Overdue')], default='Issued', null=False)

# Database Initialization
def initialize_db():
    db.connect()
    db.create_tables([Book, Member, Transaction], safe=True)
    db.close()

# Example Usage
if __name__ == "__main__":
    initialize_db()
    print("Database initialized and tables created.")
