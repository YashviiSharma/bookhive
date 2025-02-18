import csv, requests, os
from io import StringIO
from datetime import datetime
from urllib.parse import urlencode
from peewee import IntegrityError, fn
from models import Member, Book, Transaction
from flask import render_template, request, url_for, redirect, flash, Blueprint, Response


bookbp = Blueprint('book', __name__, url_prefix='/book')


@bookbp.route('/books')
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
    return render_template('bookTemplates/books.html', genres=genres)


@bookbp.route('/books/<string:genre>')
def books_by_genre(genre):
    books = Book.select().where(fn.LOWER(Book.category) == genre.lower())
    if not books.exists():
        flash("No books found in this genre.", "warning")

    return render_template('bookTemplates/genre-books.html', genre=genre, books=books)


@bookbp.route('/new-book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        return handle_add_book()

    return render_template('bookTemplates/new-book.html')


def handle_add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')
    page_count = request.form.get('page_count')
    category = request.form.get('category')
    available_copies = request.form.get('available_copies')
    rating = request.form.get('rating')
    image_url = request.form.get('image_url')

    try:
        page_count = int(page_count) if page_count else 0
        available_copies = int(available_copies) if available_copies else 0
        rating = float(rating) if rating else 0.0

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

        flash(f"Book '{title}' added successfully!", 'success')
        return redirect(url_for('book.list_books'))

    except IntegrityError:
        flash("A book with this ISBN already exists!", 'warning')
    except Exception as e:
        flash(f"Error adding book: {e}", 'danger')
        print(f"Error: {e}")

    return redirect(url_for('book.add_book'))


@bookbp.route('/list-books', methods=['GET'])
def list_books():
    books = Book.select()
    return render_template('bookTemplates/list-book.html', books=books)


@bookbp.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.get_or_none(Book.book_id == book_id)
    if book:
        book.delete_instance()
        flash("Book deleted successfully!", "success")
    else:
        flash("Book not found!", "danger")
    return redirect(url_for('book.list_books'))



@bookbp.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.get_or_none(Book.book_id == book_id)

    if request.method == 'POST':
        return handle_edit_book(book)

    return render_template('bookTemplates/edit-book.html', book=book)


def handle_edit_book(book):
    try:
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form.get('isbn')
        book.publisher = request.form.get('publisher', '')
        book.page_count = request.form.get('page_count')
        book.category = request.form.get('category', '')
        book.total_copies = int(request.form['total_copies'])
        book.available_copies = book.total_copies  # Ensure available copies match total
        book.updated_on = datetime.utcnow()
        book.save()

        flash("Book updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating book: {e}", "danger")

    return redirect(url_for('book.list_books'))


@bookbp.route('/import-books', methods=['GET', 'POST'])
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

                    existing_book = Book.get_or_none(Book.isbn == book_isbn)

                    if existing_book:
                        existing_book.total_copies += 1
                        existing_book.available_copies += 1
                        existing_book.save()

                    else:
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
                        except IntegrityError as e:
                            print(f"Integrity Error: {e}")
                            continue

                    imported_books += 1

                page += 1

            flash(f"Successfully imported {imported_books} books.", 'success')

        except Exception as e:
            flash(f"Error importing books: {e}", 'danger')

        return redirect(url_for('book.import_books'))

    books = Book.select()
    return render_template('bookTemplates/list-book.html', books=books)


@bookbp.route('/download-id-card/<int:member_id>')
def download_id_card(member_id):
    try:
        template_path = os.path.join("templates/bookTemplates/print/id_card.html")
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

        return render_template("bookTemplates/print/id_card.html", member=member, books=books, rent_fee=total_rent_fee)

    except Exception as e:
        return f"Error: {str(e)}", 500



@bookbp.route('/download-csv', methods=['GET'])
def download_csv():
    books = Book.select()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Book Title", "Author", "Available Quantity"])

    for book in books:
        writer.writerow([book.title, book.author, book.available_copies])

    output.seek(0)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=library_books.csv"

    return response
