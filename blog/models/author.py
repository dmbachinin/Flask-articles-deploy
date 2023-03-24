from flask_login import UserMixin

from blog.models.database import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Author(db.Model):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="author")
    articles = relationship("Article", back_populates="author")

    def __str__(self):
        return f"{self.user.first_name}"
