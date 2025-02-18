import csv, requests, os
from io import StringIO
from datetime import datetime
from urllib.parse import urlencode
from peewee import IntegrityError, fn
from models import supabase, create_book
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
    try:
        response = supabase.table('books').select('*').ilike('category', f"%{genre}%").execute()
        books = response.data

        if not books:
            flash("No books found in this genre.", "warning")

        return render_template('bookTemplates/genre-books.html', genre=genre, books=books)
    except Exception as e:
        flash(f"Error fetching books: {e}", "danger")
        return render_template('bookTemplates/genre-books.html', genre=genre, books=[])


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
        print("INSERTING")
        response = create_book(
            title,
            author,
            isbn,
            publisher,
            int(page_count) if page_count else 0,
            category,
            int(available_copies) if available_copies else 0,
            int(available_copies) if available_copies else 0,
            int(rating) if rating else 0,
            image_url,
        )

        return redirect('/book/list-books')
    except Exception as e:
        print(f"Error adding book: {e}", 'danger')

    return

@bookbp.route('/list-books', methods=['GET'])
def list_books():
    try:
        response = supabase.table('books').select('*').execute()
        books = response.data
        return render_template('bookTemplates/list-book.html', books=books)
    except Exception as e:
        flash(f"Error fetching books: {e}", 'danger')
        return render_template('bookTemplates/list-book.html', books=[])


@bookbp.route('/delete-book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        response = supabase.table('books').delete().eq('book_id', book_id).execute()
        print(response)
    except Exception as e:
        flash(f"Error deleting book: {e}", 'danger')

    return redirect(url_for('book.list_books'))


@bookbp.route('/edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    try:
        if request.method == 'POST':
            updated_data = {
                "title": request.form['title'],
                "author": request.form['author'],
                "isbn": request.form.get('isbn'),
                "publisher": request.form.get('publisher', ''),
                "page_count": int(request.form.get('page_count', 0)),
                "category": request.form.get('category', ''),
                "total_copies": int(request.form['total_copies']),
                "available_copies": int(request.form['total_copies']),
                "updated_on": datetime.utcnow().isoformat()
            }
            response = supabase.table('books').update(updated_data).eq('id', book_id).execute()
            if response.status_code == 200:
                flash("Book updated successfully!", "success")
            else:
                flash("Failed to update book.", "danger")
        else:
            response = supabase.table('books').select('*').eq('id', book_id).single().execute()
            book = response.data
            return render_template('bookTemplates/edit-book.html', book=book)
    except Exception as e:
        flash(f"Error updating book: {e}", "danger")

    return redirect(url_for('book.list_books'))

# def handle_edit_book(book):
#     try:
#         book.title = request.form['title']
#         book.author = request.form['author']
#         book.isbn = request.form.get('isbn')
#         book.publisher = request.form.get('publisher', '')
#         book.page_count = request.form.get('page_count')
#         book.category = request.form.get('category', '')
#         book.total_copies = int(request.form['total_copies'])
#         book.available_copies = book.total_copies  # Ensure available copies match total
#         book.updated_on = datetime.utcnow()
#         book.save()

#         flash("Book updated successfully!", "success")
#     except Exception as e:
#         flash(f"Error updating book: {e}", "danger")

#     return redirect(url_for('book.list_books'))


@bookbp.route('/import-books', methods=['GET', 'POST'])
def import_books():
    if request.method == 'POST':
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
                    print(book)
                    if imported_books >= number_of_books:
                        break

                    book_isbn = book.get('isbn')

                    # Check if the book already exists in Supabase
                    existing_book = supabase.table('books').select('*').eq('isbn', book_isbn).execute()
                    if existing_book.data:
                        # Update the existing book's copies
                        existing_data = existing_book.data[0]
                        updated_total = existing_data['total_copies'] + 1
                        updated_available = existing_data['available_copies'] + 1
                        supabase.table('books').update({
                            'total_copies': updated_total,
                            'available_copies': updated_available
                        }).eq('isbn', book_isbn).execute()

                    else:
                        # Insert a new book into Supabase
                        response = create_book(
                            book.get('title', 'Unknown Title'),
                            book.get('authors', 'Unknown Author'),
                            book_isbn,
                            book.get('publisher', 'Unknown Publisher'),
                            int(book.get('num_pages', 0)) if book.get('num_pages') else 0,
                            '',
                            1,
                            1,
                            int(book.get('average_rating', '0').split('.')[0]),
                            ''
                        )

                    imported_books += 1

                page += 1

            flash(f"Successfully imported {imported_books} books.", 'success')

        except Exception as e:
            print(f"Error importing books: {e}", 'danger')

        return redirect(url_for('book.import_books'))

    # Fetch all books from Supabase
    books = supabase.table('books').select('*').execute().data
    return render_template('bookTemplates/list-book.html', books=books)


@bookbp.route('/download-id-card/<int:member_id>')
def download_id_card(member_id):
    try:
        template_path = os.path.join("templates/bookTemplates/print/id_card.html")
        if not os.path.exists(template_path):
            return f"Template file not found at {template_path}", 500

        # Get member details from Supabase
        member = supabase.table('members').select('*').eq('id', member_id).execute().data
        if not member:
            return f"Member not found.", 404
        member = member[0]

        # Get transactions and related books for the member
        transactions = supabase.table('transactions').select('*').eq('member_id', member_id).execute().data

        books = []
        total_rent_fee = 0
        for transaction in transactions:
            book = supabase.table('books').select('*').eq('id', transaction['book_id']).execute().data
            if book:
                book = book[0]
                books.append({
                    "book_id": book['id'],
                    "title": book['title'],
                    "isbn": book['isbn'],
                    "due_date": transaction['due_date'] if transaction['due_date'] else "N/A"
                })
                total_rent_fee += 50

        return render_template("bookTemplates/print/id_card.html", member=member, books=books, rent_fee=total_rent_fee)

    except Exception as e:
        return f"Error: {str(e)}", 500


@bookbp.route('/download-csv', methods=['GET'])
def download_csv():
    # Get all books from Supabase
    books = supabase.table('books').select('title', 'author', 'available_copies').execute().data

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Book Title", "Author", "Available Quantity"])

    for book in books:
        writer.writerow([book['title'], book['author'], book['available_copies']])

    output.seek(0)

    response = Response(output.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=library_books.csv"

    return response
