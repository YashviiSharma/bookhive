
from flask import render_template, request, redirect, url_for, flash, make_response
from flask import Flask, jsonify
from models import db, Book, Member, Transaction, initialize_db
from peewee import IntegrityError, fn
from datetime import datetime
from weasyprint import HTML
import os
import requests
from urllib.parse import urlencode

app = Flask(__name__)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
@app.route('/')
def home():
    total_members = Member.select().count()
    total_books = Book.select().count()
    return render_template('homepage.html', total_members=total_members, total_books=total_books)


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
    books = Book.select().where(fn.LOWER(Book.category) == genre.lower())
    if not books.exists():
        flash("No books found in this genre.", "warning")

    return render_template('genre-books.html', genre=genre, books=books)




@app.route('/new-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        page_count = request.form.get('page_count')
        category = request.form.get('category')
        available_copies = request.form.get('available_copies')
        rating = request.form.get('rating')  # Use .get() to prevent errors
        image_url = request.form.get('image_url')

        try:
            # Convert to appropriate data types
            page_count = int(page_count) if page_count else 0
            available_copies = int(available_copies) if available_copies else 0
            rating = float(rating) if rating else 0.0

            print(f"Adding Book: {title}, ISBN: {isbn}, Copies: {available_copies}")

            # Insert book into the database
            new_book = Book.create(
                title=title,
                author=author,
                isbn=isbn,
                publisher=publisher,
                page_count=page_count,
                category=category,
                total_copies=available_copies,
                available_copies=available_copies,
                rating=rating,
                image_url=image_url
            )

            print(f"Book {new_book.title} added successfully!")

            flash(f"Book '{title}' added successfully!", 'success')
            return redirect(url_for('list_books'))

        except IntegrityError:
            flash("A book with this ISBN already exists!", 'warning')
        except Exception as e:
            flash(f"Error adding book: {e}", 'danger')
            print(f"Error: {e}")

    return render_template('new-book.html')

@app.route('/list-books', methods=['GET'])
def list_books():

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



@app.route('/import-books', methods=['GET', 'POST'])
def import_books():
    if request.method == 'POST':
        print(request.form)
        number_of_books = int(request.form.get('num_books', 20))
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        isbn = request.form.get('isbn', '').strip()
        publisher = request.form.get('publisher', '').strip()

        page = 1
        imported_books = 0

        try:
            while imported_books < number_of_books:
                # Encode parameters properly using urlencode
                params = {
                    'page': page,
                    'title': title,
                    'authors': author,
                    'isbn': isbn,
                    'publisher': publisher
                }
                api_url = f"https://frappe.io/api/method/frappe-library?{urlencode(params)}"
                print(f"Fetching API: {api_url}")

                response = requests.get(api_url)
                print(f"Response Status Code: {response.status_code}")

                if response.status_code != 200:
                    flash(f"Error fetching data from API: {response.status_code}", 'danger')
                    break

                books_data = response.json().get('message', [])
                print(f"Response JSON: {books_data}")

                if not books_data:
                    if imported_books == 0:
                        flash("No books found matching the search criteria.", 'info')
                    else:
                        flash("Finished importing available books.", 'info')
                    break

                for book in books_data:
                    if imported_books >= number_of_books:
                        break

                    book_isbn = book.get('isbn')
                    print(f"Processing book: {book.get('title')} - ISBN: {book_isbn}")

                    # Check if the book already exists
                    existing_book = Book.get_or_none(Book.isbn == book_isbn)
                    print(f"Existing book found: {existing_book}")

                    if existing_book:
                        existing_book.total_copies += 1
                        existing_book.available_copies += 1
                        existing_book.save()
                        print(f"Updated book copies for ISBN {book_isbn}")
                    else:
                        # Insert a new book entry
                        try:
                            new_book = Book.create(
                                title=book.get('title', 'Unknown Title'),
                                author=book.get('authors', 'Unknown Author'),
                                isbn=book_isbn,
                                publisher=book.get('publisher', 'Unknown Publisher'),
                                page_count=int(book.get('num_pages', 0)) if book.get('num_pages') else 0,
                                rating =int(book.get('average_rating', '0').split('.')[0]),
                                category='',
                                total_copies=1,
                                available_copies=1
                            )
                            print(f"Inserted new book: {new_book}")
                        except IntegrityError as e:
                            print(f"Integrity Error: {e}")
                            continue

                    imported_books += 1

                page += 1

            flash(f"Successfully imported {imported_books} books.", 'success')

        except Exception as e:
            flash(f"Error importing books: {e}", 'danger')
            print(f"Exception: {e}")

        return redirect(url_for('import_books'))

    books = Book.select()
    return render_template('list-book.html', books=books)



@app.route('/issue-book', methods=['GET'])
def show_issue_book_form():
    return render_template('issue-book.html')




@app.route('/issue-book', methods=['POST'])
def issue_book():
    print("Form Data Received:", request.form)
    member_id = request.form.get("member_id")
    book_ids = request.form.getlist("book_id[]")
    due_date = request.form.get("due_date")
    rent_fee_per_book = 50  # Example rent fee per book in Rs.
    current_date = datetime.now()

    if not member_id or not book_ids:
        return "Member ID and at least one Book ID are required", 400

    try:
        member = Member.get_by_id(member_id)


        fine_due = member.fine_due

        if fine_due >= 500:
            return "Member has an outstanding debt of Rs. 500 or more. Cannot issue books.", 400


        total_rent_fee = len(book_ids) * rent_fee_per_book


        total_late_fine = 0

        for book_id in book_ids:
            book = Book.get_by_id(book_id)

            if book.available_copies <= 0:
                return f"No available copies for book ID {book_id}", 400

            due_date_object = datetime.strptime(due_date, '%Y-%m-%d')

            if current_date > due_date_object:
                late_days = (current_date - due_date_object).days
                total_late_fine += late_days * 5  # Fine of ₹5 per day


            Transaction.create(
                book_id=book,
                member_id=member,
                due_date=due_date
            )

            # Reduce available copies
            book.available_copies -= 1
            book.save()

        # Update member's fine due:
        # Rent fee is always added (only once), and the fine is added based on overdue books.
        if fine_due == 0:
            member.fine_due = total_late_fine  # Only add the overdue fine (if any)
        else:
            member.fine_due += total_late_fine


        member.save()


        return redirect(url_for('issue_book_success', member_id=member_id))

    except Book.DoesNotExist:
        return "One or more books not found", 400
    except Member.DoesNotExist:
        return "Member not found", 400
    except Exception as e:
        print("Error:", str(e))
        return str(e), 500



@app.route('/issue-book-success')
def issue_book_success():
    member_id = request.args.get('member_id')
    try:
        member = Member.get_by_id(member_id)

        return render_template('issue-book-success.html', member=member, member_id=member_id)
    except Member.DoesNotExist:
        return "Member not found", 404


@app.route('/get-book/<book_id>')
def get_book(book_id):
    try:
        book = Book.get_by_id(book_id)
        return jsonify({"title": book.title})
    except Book.DoesNotExist:
        return jsonify({"error": "Book not found"}), 400


@app.route('/get-member/<int:member_id>')
def get_member(member_id):
    try:
        member = Member.get_by_id(member_id)
        return jsonify({
            "first_name": member.first_name,
            "email": member.email,
            "address": member.address,
            "phone": member.phone
        })
    except Member.DoesNotExist:
        return jsonify({"error": "Member not found"}), 404





@app.route('/download-id-card/<int:member_id>')
def download_id_card(member_id):
    try:
        template_path = os.path.join("templates/print/id_card.html")
        if not os.path.exists(template_path):
            return f"Template file not found at {template_path}", 500

        member = Member.get_by_id(member_id)
        transactions = Transaction.select().where(Transaction.member_id == member_id)

        books = []
        total_rent_fee = 0
        for transaction in transactions:
            book = Book.get_by_id(transaction.book_id)
            books.append({
                "book_id": book.book_id,
                "title": book.title,
                "isbn": book.isbn,
                "due_date": transaction.due_date.strftime("%Y-%m-%d") if transaction.due_date else "N/A"
            })
            total_rent_fee += 50


        return render_template("print/id_card.html", member=member, books=books, rent_fee=total_rent_fee)

    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/return-book/<int:transaction_id>', methods=['POST'])
def return_book(transaction_id):
    transaction = Transaction.get_or_none(Transaction.transaction_id == transaction_id)

    if not transaction:
        flash("Transaction not found!", "danger")
        return redirect(url_for('list_issued_books'))

    if transaction.status == 'Returned':
        flash("This book has already been returned.", "warning")
        return redirect(url_for('list_issued_books'))

   
    book = transaction.book_id 
    book.available_copies = fn.GREATEST(book.available_copies + 1, 0)  
    book.save()

    transaction.return_date = datetime.utcnow()
    transaction.status = 'Returned'
    transaction.save()

    flash(f"Book '{book.title}' returned successfully!", "success")
    return redirect(url_for('list_issued_books'))

@app.route('/issued-books')
def list_issued_books():
    issued_books = Transaction.select().where(Transaction.status == 'Issued')
    return render_template('issued-books.html', issued_books=issued_books)
