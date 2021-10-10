from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

# initialize app
app = Flask(__name__)

# Configure database
basedir = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Model
class Product(db.Model):
    product_code = db.Column(db.String(10), unique=True, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    price = db.Column(db.Float)

    def __init__(self, product_code, name, price):
        self.product_code = product_code
        self.name = name
        self.price = price

if __name__ == "__main__":
    app.run(debug=True)
