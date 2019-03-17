from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from forms import LoginForm, RegistrationForm, AddBook
from werkzeug.utils import secure_filename
import os
from project_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
UPLOAD_FOLDER = '/static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Main page
@app.route('/')
@app.route('/index')
def index():
    # Create list with last 5 books
    new_books = Book.query.all()[-6:]
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = session['image']
        return render_template('index.html', title='Библиотека', username=username,
                               image=image, new_book=new_books)
    return render_template('index.html', title='Библиотека', new_books=new_books)


# Sign-in page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/index')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            hash = form.password.data
            exists = Reader.query.filter_by(username=username, hash=hash).first()
            if exists:
                session['username'] = username
                session['user_id'] = exists.id
                session['image'] = exists.image
                session['admin'] = exists.admin
                return redirect('/index')
            else:
                return redirect('/login')
        return render_template('login.html', title='Авторизация', form=form)


# Registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if 'username' in session:
        pass
        session.pop('username', 0)
        session.pop('user_id', 0)
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Reader.query.filter_by(username=form.username.data).first()
        if not user:
            if form.image:
                image = form.image.data.read()
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], form.username.data))
            else:
                image = 'static/user.png'
            # Create new user
            new_user = Reader(username=form.username.data, name=form.name.data,
                              surname=form.surname.data, email=form.email.data,
                              town=form.town.data, image=image,
                              hash=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            session['user_id'] = new_user.id
            session['image'] = new_user.image
            return redirect('/index')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not session['admin']:
        return redirect('/index')
    form = AddBook()
    if form.validate_on_submit():
        book = Book.query.filter_by(name=form.name.data).first()
        if not book:
            my_file = secure_filename(form.icon.data.file.filename)
            my_file.save(os.path.join(app.config['UPLOAD_FOLDER'], form.name.data))
            icon.save(os.path.join(app.config['UPLOAD_FOLDER'], form.name.data))
            new_book = Book(name=form.name.data, author=form.author.data,
                            count_all_books=form.count_all_books.data,
                            count_book_in_lib=form.count_all_books.data, icon=icon,
                            description=form.description.data)
            new_book_primary = PrimaryBook()
            new_book.PrimaryBooks.append(new_book_primary)
            db.session.add(new_book)
            db.session.commit()
            return redirect('/success')
    username = session['username']
    image = session['image']
    return render_template('add_book.html', title='Добавить книгу', form=form, username=username, image=image)


@app.route('/success')
def success():
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = session['image']
        return render_template('success.html', title='Успех', username=username,
                               image=image)
    return render_template('success.html', title='Успех')


# Order of all book in library
@app.route('/book_order')
def book_order():
    books = Book.query.all()
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = session['image']
        return render_template('book_order.html', title='Список книг', username=username,
                               image=image, books=books)
    return render_template('book_order.html', title='Список книг', books=books)


# User's page
@app.route('/users/<user>')
def user_page(user):
    user = Reader.query.filter_by(username=user).first()
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = session['image']
        return render_template('user_page.html', title=user.name, username=username,
                               image=image, user=user)
    return render_template('user_page.html', title=user.name, user=user)


# Book's page
@app.route('/books/<book>')
def book_page(book):
    book = Book.query.filter_by(name=book).first()
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = session['image']
        return render_template('book_page.html', title=book.name, username=username,
                               image=image, book=book)
    return render_template('book_page.html', title=book.name, book=book)


###########
#   api   #
###########

class BookApi(Resource):
    def get_to_user(self, user_id, book_id):
        book = PrimaryBook.query.filter_by(id=book_id)
        reader = Reader.query.filter_by(id=user_id)
        reader.PrimaryBooks.append(book)
        db.session.commit()

    def get(self, book_id):
        return Book.query.filter_by(id=book_id)

    def delete(self, book_id):
        Book.query.filter_by(id=book_id).delete()


class ReadersApi(Resource):
    def delete_book(self, reader, book_id):
        reader = Reader.query.filter_by(username=reader).first()
        reader.PrimaryBooks.delete()


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
