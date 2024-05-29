from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    _password = Column('password', String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    DateOfBirth = Column(db.Date(), nullable=False)
    role = Column(Enum('User', 'Admin'), default='User')

    @property
    def password(self):
        raise AttributeError('Password is not readable')
    @password.setter
    def password(self, password_text):
        self._password = generate_password_hash(password_text)

    def check_password(self, password_text):
        return check_password_hash(self._password, password_text)


    def __repr__(self):
        return f'<User {self.username}>'