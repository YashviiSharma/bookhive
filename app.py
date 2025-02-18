from flask import render_template, request, redirect, url_for, flash, Flask
from models import Book, Member, initialize_db
from routes.memberRoutes import mbp


app = Flask(__name__)
app.register_blueprint(mbp)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
@app.route('/')
def home():
    total_members = Member.select().count()
    total_books = Book.select().count()
    return render_template('homepage.html', total_members=total_members, total_books=total_books)


