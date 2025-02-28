from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

# User Model
class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Changed field name for clarity
    role = db.Column(db.String(20), nullable=False)

    # Relationship: One user can have many plants
    plants = db.relationship('Plant', backref='owner', lazy=True, cascade="all, delete")

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.set_password(password)  # Hash password
        self.role = role

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    is_saved = db.Column(db.Boolean, default=False)  # Ensure default is set

    def __init__(self, name, description, is_saved=False):
        self.name = name
        self.description = description
        self.is_saved = is_saved  # Include this in the constructor

