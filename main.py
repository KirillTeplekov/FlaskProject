from flask import Flask, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from forms import LoginForm, RegistrationForm
from project_db import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
        image = Reader.filter_by(name=username).first().image
        return render_template('index.html', title='Библиотека', username=username,
                               image=image, new_book=new_books)
    else:
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
            hash = generate_password_hash(form.password.data)
            user_model = Reader()
            exists = user_model.exists(username, hash)
            if exists[0]:
                session['username'] = username
                session['user_id'] = exists[1]
                return redirect('/index')
            else:
                return redirect('/login')
        return render_template('login.html', title='Авторизация', form=form)


# Registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.image.data:
        # load custom image
        image = form.image.data
    else:
        # Load default image
        pass
    if form.validate_on_submit():
        # Create new user
        new_user = Reader(username=form.username.data, name=form.name.data,
                          surname=form.surname.data, email=form.email.data,
                          town=form.town.data, image=image,
                          hash=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


# Order of all book in library
@app.route('/book_order')
def book_order():
    books = Book.query.all()
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = Reader.filter_by(name=username).first().image
        return render_template('book_order.html', title='Список книг', username=username,
                               image=image, books=books)
    else:
        return render_template('book_order.html', title='Список книг', books=books)


# User's page
@app.route('/<username>')
def user_page(username_page):
    # Authorization check
    if 'username' in session:
        # If user authorized show user's name and image
        username = session['username']
        image = Reader.filter_by(name=username).first().image
        return render_template('user_page.html', title=username_page, username=username,
                               image=image)
    else:
        return render_template('user_page.html', title=username_page)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
