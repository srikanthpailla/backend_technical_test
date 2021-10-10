from flask import Flask, request, jsonify, json, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.exc import IntegrityError

import os

# initialize app
app = Flask(__name__)

PREFIX = "/v1"

# Configure database
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize Marshmallow serializer
marshmallow = Marshmallow(app)

# Database Model
class Product(db.Model):
    product_code = db.Column(db.String(10), unique=True, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    price = db.Column(db.Float)

    def __init__(self, product_code, name, price):
        self.product_code = product_code
        self.name = name
        self.price = price

# Serializer
class ProductSchema(marshmallow.Schema):
    class Meta:
        fields =('product_code', 'name', 'price')

# for single product
product_schema = ProductSchema()

# for multiple products
products_schema = ProductSchema(many=True)

# add product
@app.route(f'{PREFIX}/product', methods=['POST'])
def add_product():
    product_code = request.json['product_code']
    name = request.json['name']
    price = request.json['price']

    new_product = Product(product_code, name, price)
    db.session.add(new_product)
    try:
        db.session.commit()
    except IntegrityError as err:
        field = err._message().split('.')[-1]
        abort(409, description=f"Product with same {field} already exists.")

    return product_schema.jsonify(new_product)

# list all products
@app.route(f'{PREFIX}/products', methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    all_products = products_schema.dump(all_products)

    return jsonify(all_products)

# list single product
@app.route(f'{PREFIX}/product/<product_code>', methods=['GET'])
def get_single_product(product_code):
    product = Product.query.get(product_code)
    if not product:
        abort(404, description=f"Product {product_code} not found")
    return product_schema.jsonify(product)

# update a product
@app.route(f'{PREFIX}/product/<product_code>', methods=['PUT'])
def update_product(product_code):
    product = Product.query.get(product_code)
    if not product:
        abort(404, description=f"Product {product_code} not found to update")

    if request.json.get('product_code'):
        product.product_code = request.json['product_code']
    if request.json.get('name'):
        product.name = request.json['name']
    if request.json.get('price'):
        product.price = request.json['price']

    db.session.commit()

    return product_schema.jsonify(product)

# delete a product
@app.route(f'{PREFIX}/product/<product_code>', methods=['DELETE'])
def delete_product(product_code):
    product = Product.query.get(product_code)
    if not product:
        abort(404, description=f"Product {product_code} not found to delete")
    db.session.delete(product)
    db.session.commit()

    return f"Product {product_code} deleted successfully."

# Not found error
@app.errorhandler(404)
def handle_404(e):
    response = e.get_response()
    response.data = json.dumps({'message': f'{e.description}'})
    response.content_type = "application/json"
    return response

# Conflict error
@app.errorhandler(409)
def handle_409(e):
    response = e.get_response()
    response.data = json.dumps({'message': f'{e.description}'})
    response.content_type = "application/json"
    return response


# run server
if __name__ == "__main__":
    app.run(debug=True)
