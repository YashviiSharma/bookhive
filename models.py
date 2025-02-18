import os
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@dataclass
class Book:
    id: int
    title: str
    author: str
    isbn: str
    publisher: str
    page_count: int
    category: str
    total_copies: int
    available_copies: int
    rating: float
    image_url: str

# Books Functions
def create_book(title, author, isbn=None, publisher=None, page_count=None, category=None,
                total_copies=1, available_copies=1, rating=1, image_url=None):
    data = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "publisher": publisher,
        "page_count": page_count,
        "category": category,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "added_on": datetime.utcnow().isoformat(),
        "updated_on": datetime.utcnow().isoformat(),
        "rating": rating,
        "image_url": image_url
    }
    response = supabase.table("books").insert(data).execute()
    return response

def get_books():
    response = supabase.table("books").select("*").execute()
    return response.data

def get_book_by_id(book_id):
    response = supabase.table("books").select("*").eq("id", book_id).execute()
    return response.data

def update_book(book_id, **kwargs):
    kwargs["updated_on"] = datetime.utcnow().isoformat()
    response = supabase.table("books").update(kwargs).eq("book_id", book_id).execute()
    return response

def delete_book(book_id):
    response = supabase.table("books").delete().eq("book_id", book_id).execute()
    return response

# Members Functions
def create_member(first_name, last_name, email, phone, address=None, membership_type="Standard",
                  is_active=True, fine_due=0.00):
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "address": address,
        "membership_date": datetime.utcnow().isoformat(),
        "membership_type": membership_type,
        "is_active": is_active,
        "fine_due": fine_due,
        "last_updated": datetime.utcnow().isoformat()
    }
    response = supabase.table("members").insert(data).execute()
    return response

def get_members():
    response = supabase.table("members").select("*").execute()
    return response.data

def update_member(member_id, **kwargs):
    kwargs["last_updated"] = datetime.utcnow().isoformat()
    response = supabase.table("members").update(kwargs).eq("member_id", member_id).execute()
    return response

def delete_member(member_id):
    response = supabase.table("members").delete().eq("member_id", member_id).execute()
    return response

# Transactions Functions
def create_transaction(book_id, member_id, due_date, fine_amount=0.00, payment_status="Pending", status="Issued"):
    data = {
        "book_id": book_id,
        "member_id": member_id,
        "issue_date": datetime.utcnow().isoformat(),
        "due_date": due_date.isoformat(),
        "fine_amount": fine_amount,
        "payment_status": payment_status,
        "status": status
    }
    response = supabase.table("transactions").insert(data).execute()
    return response

def get_transactions():
    response = supabase.table("transactions").select("*").execute()
    return response.data

def update_transaction(transaction_id, **kwargs):
    response = supabase.table("transactions").update(kwargs).eq("transaction_id", transaction_id).execute()
    return response

def delete_transaction(transaction_id):
    response = supabase.table("transactions").delete().eq("transaction_id", transaction_id).execute()
    return response


def get_book_table():
    return supabase.table("book")

def get_members_table():
    return supabase.table("member")

def initialize_db():
    response_books = supabase.table('books').select('*', count='exact').execute()
    if response_books.data is None:
        print("'books' table not found, create it manually in Supabase.")

    response_member = supabase.table('members').select('*', count='exact').execute()
    if response_member.data is None:
        print("'members' table not found, create it manually in Supabase.")

    return len(response_books.data), len(response_member.data)

# Example Usage
if __name__ == "__main__":
    initialize_db()
