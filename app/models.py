from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Product(db.Model):
    """
    Clase producto
    attr id: la clave primaria del producto
    attr name: una descripción del producto
    attr price: precio unitario del producto
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    price = db.Column(db.Float, index=True)

    def __repr__(self):
        return '{}'.format(self.name)

    @property
    def serialize(self):
        """ Transforma el objeto en un formato serializable: return: """ 
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }


class Order(db.Model):
    """
    Clase orden
    attr id: la clave primaria de la orden
    """
    id = db.Column(db.Integer, primary_key=True)
    products = relationship('OrderProduct')

    def __repr__(self):
        return '<Order {}>'.format(self.id)

    @hybrid_property
    def orderPrice(self):
        """
        Computa el precio total de la orden
        """
        return sum([
            product.price * product.quantity for product in self.products
        ])

    @property
    def serialize(self):
        """ Transforma el objeto en un formato serializable: return: """
        return {
            'id': self.id,
            'products': [
                product.serialize for product in self.products
            ],
            'orderPrice': self.orderPrice
        }

class OrderProduct(db.Model):
    """
    Clase OrderProduct, tabla transpuesta
    """
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    product = relationship('Product')
    quantity = db.Column(db.Integer)

    @hybrid_property
    def price(self):
        return self.product.price

    @hybrid_property
    def totalPrice(self):
        """
        Computa el precio total del producto
        """
        return self.product.price * self.quantity

    @property
    def serialize(self):
        """
        Transforma el objeto en un formato serializable
        :return:
        """
        return {
            'id': self.product.id,
            'name': self.product.name,
            'price': self.product.price,
            'quantity': self.quantity,
            'totalPrice': self.totalPrice
        }
