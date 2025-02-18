from flask import render_template, request, Flask
from models import Book, Member, initialize_db
from routes.memberRoutes import mbp
from routes.bookRoutes import bookbp
from routes.transactionRoutes import tbp

app = Flask(__name__)
app.register_blueprint(mbp)
app.register_blueprint(bookbp)
app.register_blueprint(tbp)
initialize_db()

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
@app.route('/')
def home():
    total_members = Member.select().count()
    total_books = Book.select().count()
    return render_template('homepage.html', total_members=total_members, total_books=total_books)


