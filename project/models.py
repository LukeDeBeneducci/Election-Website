# IMPORTS #
from project import db, bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Defines the users table
# Contains id (primary key) - email - password(hashed) - details table foreign key
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, db.Sequence(__tablename__ + '_id_sequence'), primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    details = db.Column(db.Integer, db.Sequence(__tablename__ + '_detail_sequence'), ForeignKey('details.id'))

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<{}-{}-{}>'.format(self.id, self.email, self.password)

# Defines the details table
# Contains id (primary key) - city - age - firstname - lastname - voted - user_id relationship to User table
class Details(db.Model):

    __tablename__ = "details"

    id = db.Column(db.Integer, db.Sequence(__tablename__ + '_id_sequence'), primary_key=True)
    city = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    voted = db.Column(db.Integer, nullable=False, default=0)
    user_id = relationship("User", backref="userdeets")

    def __init__(self, city, age, first, last):
        self.city = city
        self.age = age
        self.first = first
        self.last = last
        self.voted = 0

    def __repr__(self):
        return '<{}-{}-{}-{}-{}>'.format(self.id, self.city, self.age, self.first, self.last)
