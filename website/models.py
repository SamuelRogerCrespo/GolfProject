from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Note table for storing details (shots or other notes)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))  # Title field
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))  # Foreign key to Course


# User table for main user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='owner', lazy=True)  # Relationship with Note
    addresses = db.relationship('Address', backref='owner', lazy=True)  # Relationship with Address
    phones = db.relationship('Phone', backref='owner', lazy=True)  # Relationship with Phone
    courses = db.relationship('Course', backref='owner', lazy=True)  # Relationship with Course


# Address table for storing user addresses
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150))  # Street field
    city = db.Column(db.String(100))  # City field
    state = db.Column(db.String(100))  # State field
    postal_code = db.Column(db.String(20))  # Postal code field
    country = db.Column(db.String(100))  # Country field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    address_type_id = db.Column(db.Integer, db.ForeignKey('address_type.id'))  # Foreign key to AddressType


# AddressType table for storing types of addresses (e.g., Home, Work)
class AddressType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True)  # Name of the address type (e.g., Home, Work)
    addresses = db.relationship('Address', backref='type', lazy=True)  # Relationship with Address


# Phone table for storing user phone numbers
class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20))  # Phone number field
    phone_extension = db.Column(db.String(10), nullable=True)  # Optional phone extension field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    phone_type_id = db.Column(db.Integer, db.ForeignKey('phone_type.id'))  # Foreign key to PhoneType


# PhoneType table for storing types of phone numbers (e.g., Mobile, Home)
class PhoneType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True)  # Name of the phone type (e.g., Mobile, Home)
    phones = db.relationship('Phone', backref='type', lazy=True)  # Relationship with Phone


# Course table for storing courses (golf courses or other types of courses)
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150))  # Course name field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    notes = db.relationship('Note', backref='course', lazy=True)  # Relationship with Note
