import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Resource, Api, reqparse

from src.database.models import db
from src.data import parse_data
from src.database import db_actions


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
db.init_app(app)
api = Api(app)


# with app.app_context():
#     db.create_all()
#     parse_data.get_products()


class ProductAPI(Resource):
    def row_db_to_json(self, products: list):
        data = []
        for product in products:
            data.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "img_url": product.img_url
            })

        data_json = jsonify(data)
        data_json.status_code = 201
        return data_json

    def get(self, product_id: str|None = None):
        if product_id:
            product = db_actions.get_product(product_id)
            return self.row_db_to_json([product])
        else:
            products = db_actions.get_products()
            return self.row_db_to_json(products)

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("name")
        parse.add_argument("description")
        parse.add_argument("img_url")
        parse.add_argument("price")
        args = parse.parse_args()
        prod_id = db_actions.add_product(
            name=args.get("name"),
            description=args.get("description"),
            img_url=args.get("img_url"),
            price=args.get("price")
        )
        response = jsonify(dict(product_id=prod_id))
        response.status_code - 201
        return response
    
    def put(self, product_id: str):
        parse = reqparse.RequestParser()
        parse.add_argument("name")
        parse.add_argument("description")
        parse.add_argument("price")
        parse.add_argument("img_url")
        args = parse.parse_args()
        msg = db_actions.edit_product(
            prod_id=product_id,
            name=args.get("name"),
            description=args.get("description"),
            img_url=args.get("img_url"),
            price=args.get("price")
        )
        response = jsonify(msg)
        response.status_code = 201
        return response
    
    def delete(self, product_id: str):
        msg = db_actions.del_product(product_id)
        response = jsonify(msg)
        response.status_code = 201
        return response
    

class ReviewAPI(Resource):
    def get(self, review_id):
        pass


api.add_resource(ProductAPI, "/api/products/", "/api/products/<product_id>")
api.add_resource(ReviewAPI, "/api/reviews/", "/api/reviews/<review_id>")

if __name__ == "__main__":
    app.run(debug=True, port=3000)