from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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
    pass


@app.route('/book_order')
def book_order():
    pass


@app.route('/<username>')
def user_page(username):
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
