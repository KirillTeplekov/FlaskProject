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


@app.route('/')
@app.route('/index')
def index():
    pass


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        hash = generate_password_hash(form.password.data)
        user_model = Reader()
        exists = user_model.exists(user_name, hash)
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect('/index')
        else:
            return redirect('/login')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration')
def registration():
    pass


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/book_order')
def book_order():
    pass


@app.route('/<username>')
def user_page(username):
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
