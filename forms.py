from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


# Form for sig-in page
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


# Form for registration page
class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    town = StringField('Город(не обязательно к заполнению)')
    image = FileField('Загрузите изображение(только .png)', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


# Form for add_book page
class AddBook(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    count_all_books = IntegerField('Число книг', validators=[DataRequired()])
    icon = FileField('Загрузите изображение', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Создать')
