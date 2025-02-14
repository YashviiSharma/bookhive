

from flask import render_template, request, redirect, url_for, flash
from flask import Flask, jsonify
from models import db, Book, Member, Transaction, initialize_db
from peewee import IntegrityError
from datetime import datetime


app = Flask(__name__)

# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost/library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_app(app)

@app.route("/")
def index():
    return "Home Page"

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'

@app.route('/')
def home():
    return render_template('homepage.html')



@app.route('/new-book', methods=['GET','POST'])
def add_book():
    # Extract form data
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')
    page_count = request.form.get('page_count')
    category = request.form.get('category')
    total_copies = request.form.get('total_copies')

    try:
        # Add new book to the database
        new_book = Book.create(
            title=title,
            author=author,
            isbn=isbn,
            publisher=publisher,
            page_count=int(page_count) if page_count else None,
            category=category,
            total_copies=int(total_copies),
            available_copies=int(total_copies)
        )
        flash(f"Book '{title}' added successfully!", 'success')
    except Exception as e:
        flash(f"Error adding book: {e}", 'danger')

    # Redirect back to the homepage or another page
    return render_template('new-book.html')

@app.route('/books', methods=['GET'])
def list_books():
    # Fetch all books from the database using Peewee
    books = Book.select()
    return render_template('list-book.html', books=books)



@app.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.get_or_none(Book.book_id == book_id)
    if book:
        book.delete_instance()
        flash("Book deleted successfully!", "success")
    else:
        flash("Book not found!", "danger")
    return redirect(url_for('list_books'))



@app.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.get_or_none(Book.book_id == book_id)
    if not book:
        flash("Book not found!", "danger")
        return redirect(url_for('list_books'))

    if request.method == 'POST':
        try:
            book.title = request.form['title']
            book.author = request.form['author']
            book.isbn = request.form.get('isbn', None)
            book.publisher = request.form.get('publisher', '')
            book.page_count = request.form.get('page_count', None)
            book.category = request.form.get('category', '')
            book.total_copies = int(request.form['total_copies'])
            book.available_copies = book.total_copies  # Ensure available copies match total
            book.updated_on = datetime.utcnow()
            book.save()
            flash("Book updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating book: {e}", "danger")
        return redirect(url_for('list_books'))

    return render_template('edit-book.html', book=book)


import requests  # Import the requests library for API calls

@app.route('/import-books', methods=['GET', 'POST'])
def import_books():
    if request.method == 'POST':
        # Extract parameters from the form
        number_of_books = int(request.form.get('number_of_books', 20))
        title = request.form.get('title', '')
        author = request.form.get('author', '')
        isbn = request.form.get('isbn', '')
        publisher = request.form.get('publisher', '')
        page = 1  # Start from page 1

        imported_books = 0  # Counter for successfully imported books

        try:
            while imported_books < number_of_books:
                # Make an API request
                api_url = f"https://frappe.io/api/method/frappe-library?page={page}&title={title}&author={author}&isbn={isbn}&publisher={publisher}"
                response = requests.get(api_url)

                if response.status_code != 200:
                    flash(f"Error fetching data from API: {response.status_code}", 'danger')
                    break

                # Parse the JSON response
                books_data = response.json().get('message', [])
                if not books_data:
                    flash("No more books available to fetch.", 'info')
                    break

                for book in books_data:
                    if imported_books >= number_of_books:
                        break  # Stop if the required number of books is reached

                    # Check if the book already exists
                    existing_book = Book.get_or_none(Book.isbn == book.get('isbn'))
                    if existing_book:
                        # Update the total_copies and available_copies
                        copies_to_add = min(number_of_books - imported_books, 1)  # Add only up to the remaining needed books
                        existing_book.total_copies += copies_to_add
                        existing_book.available_copies += copies_to_add
                        existing_book.save()
                        imported_books += copies_to_add
                    else:
                        try:
                            # Insert a new book into the database
                            copies_to_add = min(number_of_books - imported_books, 1)
                            Book.create(
                                title=book.get('title'),
                                author=book.get('authors'),
                                isbn=book.get('isbn'),
                                publisher=book.get('publisher'),
                                page_count=int(book.get('num_pages', 0)) if book.get('num_pages') else 0,
                                category='',  # Optional: Can be set based on your app logic
                                total_copies=copies_to_add,
                                available_copies=copies_to_add
                            )
                            imported_books += copies_to_add
                        except IntegrityError:
                            # Skip if there's an issue with adding the book
                            continue

                page += 1  # Move to the next page

            flash(f"Successfully imported {imported_books} books.", 'success')

        except Exception as e:
            flash(f"Error importing books: {e}", 'danger')

    return redirect(url_for('list_books'))
