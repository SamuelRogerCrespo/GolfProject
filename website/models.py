from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Note table for storing details (shots or other notes)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)  # Title field
    data = db.Column(db.String(10000), nullable=False)  # Note content
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)  # Foreign key to Course

    def __repr__(self):
        return f'<Note {self.title}>'

# User table for main user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)  # Add last name field
    notes = db.relationship('Note', backref='owner', lazy=True)  # Relationship with Note
    addresses = db.relationship('Address', backref='owner', lazy=True)  # Relationship with Address
    phones = db.relationship('Phone', backref='owner', lazy=True)  # Relationship with Phone
    courses = db.relationship('Course', backref='owner', lazy=True)  # Relationship with Course

    def __repr__(self):
        return f'<User {self.email}>'


# Address table for storing user addresses
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150), nullable=False)  # Street field
    city = db.Column(db.String(100), nullable=False)  # City field
    state = db.Column(db.String(100), nullable=False)  # State field
    postal_code = db.Column(db.String(20), nullable=False)  # Postal code field
    country = db.Column(db.String(100), nullable=False)  # Country field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    address_type_id = db.Column(db.Integer, db.ForeignKey('address_type.id'), nullable=True)  # Foreign key to AddressType

    def __repr__(self):
        return f'<Address {self.street}, {self.city}>'

# AddressType table for storing types of addresses (e.g., Home, Work)
class AddressType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)  # Name of the address type (e.g., Home, Work)
    addresses = db.relationship('Address', backref='type', lazy=True)  # Relationship with Address

    def __repr__(self):
        return f'<AddressType {self.type_name}>'

# Phone table for storing user phone numbers
class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)  # Phone number field
    phone_extension = db.Column(db.String(10), nullable=True)  # Optional phone extension field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    phone_type_id = db.Column(db.Integer, db.ForeignKey('phone_type.id'), nullable=True)  # Foreign key to PhoneType

    def __repr__(self):
        return f'<Phone {self.phone_number}>'

# PhoneType table for storing types of phone numbers (e.g., Mobile, Home)
class PhoneType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)  # Name of the phone type (e.g., Mobile, Home)
    phones = db.relationship('Phone', backref='type', lazy=True)  # Relationship with Phone

    def __repr__(self):
        return f'<PhoneType {self.type_name}>'

# Course table for storing courses (golf courses or other types of courses)
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)  # Course name field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    notes = db.relationship('Note', backref='course', lazy=True)  # Relationship with Note

    def __repr__(self):
        return f'<Course {self.course_name}>'
