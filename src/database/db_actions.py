from uuid import uuid4
from typing import List

from src.database.models import db, Product, Review


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


def add_review_by_product(review: Review, prod_id: str) -> str:
    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    product.reviews.append(review)
    db.session.commit
    return "Successful"

def add_review(text) -> str:
    review = Review(text=text, id=uuid4().hex)
    review.reviews.append(review)
    db.add(review)
    db.session.commit
    return "Successful"


def edit_review(
        rev_id: str,
        content: str,
        rating: str,
) -> str:
    review = db.one_or_404(db.session.query(Review)).where(Review.id == rev_id)
    review.content = content
    review.rating = rating
    db.session.commit()
    return "Successful"


def get_review(review_id: str) -> Review:
    return db.session.query(Review).filter_by(id=review_id).first()


def del_review(review_id) -> str:
    review = db.session.query(Review).filter_by(id=review_id).first()
    db.session.delete(review)
    db.session.commit()
    return "Successful"
