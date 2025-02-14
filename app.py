
from flask import render_template, request, redirect, url_for, flash
from flask import Flask, jsonify
from models import db, Book, Member, Transaction, initialize_db
<<<<<<< HEAD
from peewee import IntegrityError
from datetime import datetime

=======
>>>>>>> a682e7b452566a69da0453d12a84e734210b6c19

app = Flask(__name__)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
<<<<<<< HEAD

=======
>>>>>>> a682e7b452566a69da0453d12a84e734210b6c19
@app.route('/')
def home():
    total_members = Member.select().count()
    return render_template('homepage.html', total_members=total_members)


@app.route('/new-member', methods=['GET', 'POST'])
def new_member():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form.get('address', '')

        try:
            # Create and save a new Member instance
            new_member = Member.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )
            flash("Member added successfully!", "success")
            return redirect(url_for('list_member'))
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template('new-member.html')


@app.route('/list-member')
def list_member():
    members = Member.select()
    return render_template('list-member.html', members=members)



@app.route('/edit-member/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.get_or_none(Member.member_id == member_id)
    if not member:
        flash("Member not found!", "danger")
        return redirect(url_for('list_member'))

    if request.method == 'POST':
        member.first_name = request.form['first_name']
        member.last_name = request.form['last_name']
        member.email = request.form['email']
        member.phone = request.form['phone']
        member.address = request.form.get('address', '')
        member.save()
        flash("Member updated successfully!", "success")
        return redirect(url_for('list_member'))

    return render_template('edit-member.html', member=member)

@app.route('/delete-member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.get_or_none(Member.member_id == member_id)
    if member:
        member.delete_instance()
        flash("Member deleted successfully!", "success")
    else:
        flash("Member not found!", "danger")
    return redirect(url_for('list_member'))

@app.route('/books')
def books():
    genres = {
        "Fiction": "https://i0.wp.com/joncronshaw.com/wp-content/uploads/2023/12/DALL%C2%B7E-2023-12-05-10.05.23-A-majestic-wyvern-soaring-above-a-breathtaking-fantasy-landscape.-The-wyvern-a-large-dragon-like-creature-with-two-legs-and-a-pair-of-large-wings-g.png?fit=1200%2C686&ssl=1",
        "Sci-Fi": "https://cdn.britannica.com/09/92009-050-122EC720/Enterprise-from-Star-Trek-III-The-Search.jpg",
        "Horror": "https://t3.ftcdn.net/jpg/03/77/93/14/360_F_377931465_txu2WCMcmQL87ARK6ztPP2Udor5waNDJ.jpg",
        "Romantic": "https://cdn.marcusashley.com/wp-content/uploads/2021/08/06095341/tuesdays-child-painting-michael-parkes.jpg",
        "Comedy": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQx0Uc1PA12zdXqfrEh0l-8Ka0vCYD6JazVIQ&s",
        "Mystery": "https://upload.wikimedia.org/wikipedia/commons/7/78/Mystery_January_1934.jpg",
        "Fantasy": "https://rukminim2.flixcart.com/image/850/1000/l0e6kcw0/poster/o/3/w/medium-digital-painting-wall-hd-wallpaper-art-paper-fantasy-original-imagc6xwjkztywzb.jpeg?q=90&crop=false",
        "Thriller": "https://m.media-amazon.com/images/M/MV5BOTIxNjg1YTYtZjExNi00YWIwLTlmNGMtNjdkODc5NTc4ZmYzXkEyXkFqcGc@._V1_.jpg",
        "Biography": "https://m.media-amazon.com/images/I/510phaa3WTL._SL500_.jpg",
        "History": "https://celadonbooks.com/wp-content/uploads/2020/03/Historical-Fiction-1024x596.jpg",
    }
    return render_template('books.html', genres=genres)


@app.route('/books/<string:genre>')
def books_by_genre(genre):
    books = Book.select().where(Book.category == genre)  # Use `category` instead of `genre`
    
    if not books.exists():
        flash("No books found in this genre.", "warning")
    
    return render_template('genre-books.html', genre=genre, books=books)




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
