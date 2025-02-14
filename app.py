
from flask import render_template, request, redirect, url_for, flash
from flask import Flask, jsonify
from models import db, Book, Member, Transaction, initialize_db

app = Flask(__name__)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
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


