from sqlalchemy import Integer, Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from blog.models.database import db

article_tag_associations_table = Table(
    "article_tag_associations",
    db.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tags.id"), nullable=False)
)


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    articles = relationship("Article", secondary=article_tag_associations_table, back_populates="tags")

    def __str__(self):
        return f"{self.name}"

