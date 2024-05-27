from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'

    UserID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    DateOfBirth = Column(db.Date(), nullable=False)
    role = Column(Enum('User', 'Admin'), default='User')