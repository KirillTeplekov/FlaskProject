from main import db


# Associative table for creating relationships inter reader and book
class Associative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book = db.relationship("Book", backref=db.backref("Associatives", lazy=True))
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'))
    reader = db.relationship("Reader", backref=db.backref("Associatives", lazy=True))


# Reader table
class Reader(db.Model):
    __tablename__ = 'readers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    town = db.Column(db.String(80), unique=False, nullable=True)
    image = db.Column(db.String(150), nullable=False)
    hash = db.Column(db.String(120), unique=True, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Reader {} {} {} {}>'.format(
            self.id, self.username, self.name, self.surname)


# Book table
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    count_all_books = db.Column(db.Integer, nullable=False)
    count_book_in_lib = db.Column(db.Integer, nullable=False)
    icon = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<Book {} {} {} {}>'.format(
            self.id, self.name, self.author, self.count_book_in_lib)


# Review table
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(80), unique=False, nullable=False)
    text = db.Column(db.String(500), unique=False, nullable=False)

    # Create relationship inter review and reader
    reader_id = db.Column(db.Integer,
                          db.ForeignKey('readers.id'),
                          nullable=False)
    reader = db.relationship('Reader',
                             backref=db.backref('Reviews',
                                                lazy=True))

    # Create relationship inter review and book
    book_id = db.Column(db.Integer,
                        db.ForeignKey('books.id'),
                        nullable=False)
    book = db.relationship('Book',
                           backref=db.backref('Reviews',
                                              lazy=True))

    def __repr__(self):
        return '<Review {} {} {} {}>'.format(
            self.id, self.header, self.text, self.reader)
