from peewee import fn
from datetime import datetime
from models import Member, Book, Transaction
from flask import render_template, request, url_for, redirect, flash, Blueprint, jsonify

tbp = Blueprint('transaction', __name__, url_prefix='/transaction')

@tbp.route('/issue-book', methods=['GET'])
def show_issue_book_form():
    return render_template('bookTemplates/issue-book.html')


@tbp.route('/issue-book', methods=['POST'])
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


        fine_due = int(member.fine_due)

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


        return redirect(url_for('transaction.issue_book_success', member_id=member_id))

    except Book.DoesNotExist:
        return "One or more books not found", 400
    except Member.DoesNotExist:
        return "Member not found", 400
    except Exception as e:
        print("Error:", str(e))
        return str(e), 500



@tbp.route('/issue-book-success')
def issue_book_success():
    member_id = request.args.get('member_id')
    try:
        member = Member.get_by_id(member_id)

        return render_template('bookTemplates/issue-book-success.html', member=member, member_id=member_id)
    except Member.DoesNotExist:
        return "Member not found", 404


@tbp.route('/get-book/<book_id>')
def get_book(book_id):
    try:
        book = Book.get_by_id(book_id)
        return jsonify({"title": book.title})
    except Book.DoesNotExist:
        return jsonify({"error": "Book not found"}), 400


@tbp.route('/get-member/<int:member_id>')
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


@tbp.route('/return-book/<int:transaction_id>', methods=['POST'])
def return_book(transaction_id):
    transaction = Transaction.get_or_none(Transaction.transaction_id == transaction_id)

    if not transaction:
        flash("Transaction not found!", "danger")
        return redirect(url_for('transaction.list_issued_books'))

    if transaction.status == 'Returned':
        flash("This book has already been returned.", "warning")
        return redirect(url_for('transaction.list_issued_books'))


    book = transaction.book_id
    book.available_copies = fn.GREATEST(book.available_copies + 1, 0)
    book.save()

    transaction.return_date = datetime.utcnow()
    transaction.status = 'Returned'
    transaction.save()

    flash(f"Book '{book.title}' returned successfully!", "success")
    return redirect(url_for('transaction.list_issued_books'))

@tbp.route('/issued-books')
def list_issued_books():
    issued_books = Transaction.select().where(Transaction.status == 'Issued')
    return render_template('bookTemplates/issued-books.html', issued_books=issued_books)
