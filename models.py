from database import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    published_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float, nullable=False)

