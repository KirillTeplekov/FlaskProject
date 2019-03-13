from main import db


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    town = db.Column(db.String(80), unique=False, nullable=True)
    book_order = db.Column(db.List, nullable=True)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Reader {} {} {} {}>'.format(
            self.id, self.username, self.name, self.surname)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    count_all_books = db.Column(db.Integer, nullable=False)
    count_book_in_lib = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.LargeBinary)
    discription = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<Book {} {} {} {}>'.format(
            self.id, self.name, self.author, self.count_book_in_lib)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.String(500), unique=False, nullable=False)
    reader_id = db.Column(db.Integer,
                          db.ForeignKey('reader.id'),
                          nullable=False)
    reader = db.relationship('Reader',
                             backref=db.backref('Reviews',
                                                lazy=True))

    def __repr__(self):
        return '<Review {} {} {} {}>'.format(
            self.id, self.header, self.text, self.reader)
