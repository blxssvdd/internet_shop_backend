from uuid import uuid4
from typing import List

from src.database.models import Product, Review, User
from src.database.base import db


def get_products() -> List[Product]:
    # return db.get_or_404(db.session.query(Product))
    return db.session.query(Product).all()


def get_product(prod_id: str) -> Product:
    return db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    # return db.session.query(Product).where(Product.id == prod_id).first()


def add_product(
    name: str,
    description: str,
    img_url: str,
    price: float
) -> str:
    product = Product(
        id=uuid4().hex,
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product.id


def edit_product(
        prod_id: str,
        name: str,
        description: str,
        img_url: str,
        price: float
) -> str:
    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    product.name = name
    product.description = description
    product.img_url = img_url
    product.price = price
    db.session.commit()
    return "Successful"


def del_product(prod_id: str) -> str:
    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    db.session.delete(product)
    db.session.commit()
    return "Successful"

# ВІДГУКИ

def get_reviews() -> List[Review]:
    return db.session.query(Review).all()


def get_review(review_id: str) -> Review:
    return db.one_or_404(db.session.query(Review).where(Review.id == review_id))


def add_review(
    text: str,
    author: str,
    rating: float
) -> str:
    review = Review(
        id=uuid4().hex,
        text=text,
        author=author,
        rating=rating
    )
    db.session.add(review)
    db.session.commit()
    db.session.refresh(review)
    return review.id


def edit_review(
        rev_id: str,
        text: str,
        author: str,
        rating: float
) -> str:
    review = db.one_or_404(db.session.query(Review).where(Review.id == rev_id))
    review.text = text
    review.author = author
    review.rating = rating
    db.session.commit()
    return "Successful"


def del_review(rev_id: str) -> str:
    review = db.one_or_404(db.session.query(Review).where(Review.id == rev_id))
    db.session.delete(review)
    db.session.commit()
    return "Successful"


def add_user(
    email: str,
    password: str,
    first_name: str|None = None,
    last_name: str|None = None
) -> str:
    user = User(
        id=uuid4().hex,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return "Successful"


def get_user(user_id: str):
    return db.one_or_404(db.session.query(User).where(User.id==user_id))


def get_tokens(email: str, password: str) -> dict|None:
    user = db.one_or_404(db.session.query(User).where(User.email==email))
    return user.get_tokens(password)