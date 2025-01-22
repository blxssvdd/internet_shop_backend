from uuid import uuid4
from typing import List

from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship
from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()
db = SQLAlchemy(model_class=Base, engine_options=dict(echo=True))


rev_prod_assoc = Table(
    "rev_prod_assoc",
    Base.metadata,
    Column("review_id", ForeignKey("reviews.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(), primary_key=True, default=uuid4().hex)
    text: Mapped[str] = mapped_column(String())
    rating: Mapped[float] = mapped_column()
    author: Mapped[str] = mapped_column(String())


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    img_url: Mapped[str] = mapped_column(String())
    price: Mapped[float] = mapped_column()
    reviews: Mapped[List[Review]] = relationship(secondary=rev_prod_assoc)