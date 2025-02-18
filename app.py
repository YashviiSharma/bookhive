from flask import render_template, request, Flask
from models import initialize_db, get_book_table
from routes.bookRoutes import bookbp
# from routes.memberRoutes import mbp
# from routes.transactionRoutes import tbp

app = Flask(__name__)
# app.register_blueprint(mbp)
app.register_blueprint(bookbp)
# app.register_blueprint(tbp)

if __name__ == '__main__':
    app.run(debug=True)

app.secret_key = 'x/x/x/x/x/x/x/x/x/x/x/x/x//s//s/s/s/s/s/'
@app.route('/')
def home():
    total_books, total_members = initialize_db()
    return render_template('homepage.html', total_members=total_members, total_books=total_books)
