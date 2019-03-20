from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from forms import LoginForm, RegistrationForm, AddBook
from requests import get, delete
import os
from project_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Main page
@app.route('/')
@app.route('/index')
def index():
    # Create list with last 5 books
    new_books = Book.query.all()[-3:]
    return render_template('index.html', title='Библиотека', new_books=new_books, image='static\lib_photo.png')


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
        # Check for the existence of the user in db
        user = Reader.query.filter_by(username=form.username.data).first()
        if not user:
            if form.image:
                try:
                    image_name = os.path.join(app.config['UPLOAD_FOLDER'] + form.username.data + '.png')
                    with open(image_name, 'wb') as file:
                        file.write(form.image.data.read())
                        file.close()
                except Exception as e:
                    return render_template('error_page.html', title='Ошибка', error=e)
            else:
                image_name = 'static/user.png'

            # Create new user
            new_user = Reader(username=form.username.data, name=form.name.data,
                              surname=form.surname.data, email=form.email.data,
                              town=form.town.data, image=image_name,
                              hash=form.password.data, admin=False)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            session['user_id'] = new_user.id
            session['image'] = new_user.image
            return redirect('/index')
        else:
            return render_template('error_page.html', title='Ошибка', error='Такой пользователь уже существует')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    session['admin'] = False
    return redirect('/login')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if not session['admin']:
        return redirect('/index')
    form = AddBook()
    if form.validate_on_submit():
        book = Book.query.filter_by(name=form.name.data).first()
        if not book:
            try:
                icon_name = os.path.join(app.config['UPLOAD_FOLDER'] + form.name.data + '.png')
                with open(icon_name, 'wb') as icon:
                    icon.write(form.icon.data.read())
                    icon.close()
            except Exception as e:
                return render_template('error_page.html', title='Ошибка', error=e)

            # Add new book in db
            new_book = Book(name=form.name.data, author=form.author.data,
                            count_all_books=form.count_all_books.data,
                            count_book_in_lib=form.count_all_books.data, icon=icon_name,
                            description=form.description.data)
            db.session.add(new_book)
            db.session.commit()
            return redirect('/success')
        else:
            return render_template('error_page.html', title='Ошибка', error='Книга уже была создана')
    return render_template('add_book.html', title='Добавить книгу', form=form)


@app.route('/success')
def success():
    return render_template('success.html', title='Успех')


# Order of all book in library
@app.route('/book_order')
def book_order():
    books = Book.query.all()
    return render_template('book_order.html', title='Список книг', books=books)


# User's page
@app.route('/users/<user>')
def user_page(user):
    user = Reader.query.filter_by(username=user).first()
    rows = Associative.query.filter_by(reader_id=user.id)
    book_order = []
    for row in rows:
        book_order.append(Book.query.filter_by(associative=row.id).first())
    if user:
        return render_template('user_page.html', title=user.usernamename, user=user, book_order=book_order, delete=delete)
    else:
        return render_template('error_page.html', title='Ошибка', error='Такого пользователя нет')


# Book's page
@app.route('/books/<book>')
def book_page(book):
    book = Book.query.filter_by(name=book).first()
    return render_template('book_page.html', title=book.name, book=book)


###########
#   api   #
###########

class BookApi(Resource):
    # Add get to User
    def get(self, book_id, user_id):
        associative = Associative()
        book = Book.query.filter_by(id=book_id)
        book.Associatives.append(associative)
        reader = Reader.query.filter_by(id=user_id)
        reader.Associatives.append(associative)
        book.count_book_in_lib -= 1
        db.session.add(associative)
        db.session.commit()

    # Delete book from library
    def delete(self, book_id, user_id):
        Book.query.filter_by(id=book_id).first().delete()


class ReaderApi(Resource):
    # Delete book from user's order
    def get(self, user_id, book_id):
        Associative.query.filter_by(reader_id=user_id, book_id=book_id).delete()
        Book.query.filter_by(id=book_id).first().count_in_lib += 1


api.add_resource(BookApi, '/books/<int:book_id>/<int:user_id>')
api.add_resource(ReaderApi, '/users/<int:user_id>/<int:book_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(port=8080, host='127.0.0.1')
