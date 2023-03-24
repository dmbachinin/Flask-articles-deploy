from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from blog.models.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    is_staff = Column(Boolean, nullable=False, default=False)
    password = Column(String(255), nullable=False)

    author = relationship("Author", uselist=False, back_populates="user")

    def __str__(self):
        return f"{self.email}"

    def __int__(self, first_name, last_name, email, is_staff, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_staff = is_staff
        self.password = password

