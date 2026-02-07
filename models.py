from app import db
from datetime import datetime
from flask_login import UserMixin

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref=db.backref('user', lazy=True))

# Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationships
    books = db.relationship('Book', backref=db.backref('category', lazy=True))

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Relationships
    borrow_records = db.relationship('BorrowRecord', backref=db.backref('book', lazy=True))

# BorrowRecord model
class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='borrowed')  # borrowed, returned, overdue
    
    def __init__(self, user_id, book_id, due_date):
        self.user_id = user_id
        self.book_id = book_id
        self.due_date = due_date
        
        # Update book availability
        book = Book.query.get(book_id)
        if book:
            book.available = False
            db.session.commit()
    
    def return_book(self):
        self.return_date = datetime.utcnow()
        self.status = 'returned'
        
        # Update book availability
        book = Book.query.get(self.book_id)
        if book:
            book.available = True
            db.session.commit()