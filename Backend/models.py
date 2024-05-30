from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    # Set the table name Users
    __tablename__ = 'Users'
    # Define columns for the Users table
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    _password = Column('password', String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    DateOfBirth = Column(db.Date(), nullable=False)
    role = Column(Enum('User', 'Admin'), default='User')

    # Prevents password being read directly
    @property
    def password(self):
        raise AttributeError('Password is not readable')

    # Hashes password before storing it
    @password.setter
    def password(self, password_text):
        self._password = generate_password_hash(password_text)

    # Method to if the password matches the stored hashed password
    def check_password(self, password_text):
        return check_password_hash(self._password, password_text)


    def __repr__(self):
        return f'<User {self.username}>'