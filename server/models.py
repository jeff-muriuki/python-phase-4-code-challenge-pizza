from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    pizzas= db.relationship('RestaurantPizza', backref='restaurant', lazy=True, cascade='all, delete-orphan')

    # add serialization rules
    serialize_only= ('id', 'name', 'address')

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurants= db.relationship('RestaurantPizza', backref='pizza', lazy=True)

    # add serialization rules
    serialize_only= ('id', 'name', 'ingredients')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    pizza_id= db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id= db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    # add serialization rules
    serialize_only= ('id', 'price', 'pizza_id', 'restaurant_id', 'pizza', 'restaurant')
    
    # add validation
    @validates('price')
    def validates_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError('price must be...')
        return price
    
    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
