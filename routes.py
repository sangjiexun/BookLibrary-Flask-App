from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db
from models import User, Category, Book, BorrowRecord
from forms import LoginForm, RegistrationForm, BookForm, BorrowForm, CategoryForm, SearchForm
from datetime import datetime, timedelta

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # In production, use hashed passwords
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # In production, use hashed passwords
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

# Index route
@app.route('/index')
@login_required
def index():
    # Get recent books
    recent_books = Book.query.order_by(Book.id.desc()).limit(5).all()
    
    # Get user's borrowed books
    borrowed_books = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').all()
    
    return render_template('index.html', title='Home', recent_books=recent_books, borrowed_books=borrowed_books)

# Books route
@app.route('/books')
@login_required
def books():
    # Get all books
    books = Book.query.all()
    
    return render_template('books.html', title='Books', books=books)

# Book detail route
@app.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', title=book.title, book=book)

# Borrow book route
@app.route('/borrow/<int:book_id>', methods=['GET', 'POST'])
@login_required
def borrow(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if book is available
    if not book.available:
        flash('Book is not available for borrowing', 'danger')
        return redirect(url_for('book_detail', book_id=book_id))
    
    form = BorrowForm()
    if form.validate_on_submit():
        # Create borrow record
        borrow_record = BorrowRecord(
            user_id=current_user.id,
            book_id=book_id,
            due_date=form.due_date.data
        )
        db.session.add(borrow_record)
        db.session.commit()
        flash('Book has been borrowed', 'success')
        return redirect(url_for('my_books'))
    
    # Set default due date (2 weeks from today)
    form.due_date.data = datetime.utcnow() + timedelta(weeks=2)
    
    return render_template('borrow.html', title='Borrow Book', book=book, form=form)

# Return book route
@app.route('/return/<int:borrow_id>')
@login_required
def return_book(borrow_id):
    borrow_record = BorrowRecord.query.get_or_404(borrow_id)
    
    # Check if current user is the borrower
    if borrow_record.user_id != current_user.id:
        flash('You can only return books you borrowed', 'danger')
        return redirect(url_for('my_books'))
    
    # Check if book is already returned
    if borrow_record.status == 'returned':
        flash('Book has already been returned', 'info')
        return redirect(url_for('my_books'))
    
    # Return the book
    borrow_record.return_book()
    db.session.commit()
    flash('Book has been returned', 'success')
    return redirect(url_for('my_books'))

# My books route
@app.route('/my_books')
@login_required
def my_books():
    # Get user's borrow records
    borrow_records = BorrowRecord.query.filter_by(user_id=current_user.id).order_by(BorrowRecord.borrow_date.desc()).all()
    
    return render_template('my_books.html', title='My Books', borrow_records=borrow_records)

# Admin route
@app.route('/admin')
@login_required
def admin():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    # Get statistics
    total_books = Book.query.count()
    available_books = Book.query.filter_by(available=True).count()
    borrowed_books = BorrowRecord.query.filter_by(status='borrowed').count()
    total_users = User.query.count()
    
    return render_template('admin.html', title='Admin Panel', 
                         total_books=total_books, 
                         available_books=available_books, 
                         borrowed_books=borrowed_books, 
                         total_users=total_users)

# Add book route
@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    form = BookForm()
    
    # Populate category choices
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data,
            publish_date=form.publish_date.data,
            description=form.description.data,
            quantity=form.quantity.data,
            category_id=form.category_id.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book has been added', 'success')
        return redirect(url_for('books'))
    
    return render_template('add_book.html', title='Add Book', form=form)

# Edit book route
@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    
    # Populate category choices
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.publisher = form.publisher.data
        book.publish_date = form.publish_date.data
        book.description = form.description.data
        book.quantity = form.quantity.data
        book.category_id = form.category_id.data
        
        db.session.commit()
        flash('Book has been updated', 'success')
        return redirect(url_for('book_detail', book_id=book_id))
    
    return render_template('add_book.html', title='Edit Book', form=form)

# Delete book route
@app.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    book = Book.query.get_or_404(book_id)
    
    # Check if book is borrowed
    borrowed_records = BorrowRecord.query.filter_by(book_id=book_id, status='borrowed').all()
    if borrowed_records:
        flash('Cannot delete book that is currently borrowed', 'danger')
        return redirect(url_for('book_detail', book_id=book_id))
    
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted', 'success')
    return redirect(url_for('books'))

# Categories route
@app.route('/categories')
@login_required
def categories():
    # Get all categories
    categories = Category.query.all()
    
    return render_template('categories.html', title='Categories', categories=categories)

# Add category route
@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category has been added', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html', title='Add Category', form=form)

# Edit category route
@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        
        db.session.commit()
        flash('Category has been updated', 'success')
        return redirect(url_for('categories'))
    
    return render_template('add_category.html', title='Edit Category', form=form)

# Delete category route
@app.route('/delete_category/<int:category_id>')
@login_required
def delete_category(category_id):
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(category_id)
    
    # Check if category has books
    if category.books:
        flash('Cannot delete category that has books', 'danger')
        return redirect(url_for('categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted', 'success')
    return redirect(url_for('categories'))

# Search route
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    books = []
    
    if form.validate_on_submit():
        search_term = form.search.data
        
        # Search in book titles, authors, and descriptions
        books = Book.query.filter(
            db.or_(
                Book.title.ilike(f'%{search_term}%'),
                Book.author.ilike(f'%{search_term}%'),
                Book.description.ilike(f'%{search_term}%')
            )
        ).all()
    
    return render_template('search.html', title='Search', form=form, books=books)

# Users route
@app.route('/users')
@login_required
def users():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    # Get all users
    users = User.query.all()
    
    return render_template('users.html', title='Users', users=users)

# Overdue books route
@app.route('/overdue')
@login_required
def overdue():
    # Check if user is admin
    if not current_user.is_admin:
        flash('You do not have admin privileges', 'danger')
        return redirect(url_for('index'))
    
    # Get overdue books
    today = datetime.utcnow()
    overdue_records = BorrowRecord.query.filter(
        BorrowRecord.due_date < today,
        BorrowRecord.status == 'borrowed'
    ).all()
    
    return render_template('overdue.html', title='Overdue Books', overdue_records=overdue_records)