import os
import unittest

from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"

    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Falló el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")

    def test_metodo_put(self):
        o=Order(id=1)
        db.session.add(o)
        p=Product(name="cuchara" ,price=25)
        db.session.add(p)
        orderP=OrderProduct(order_id=1, product_id=1 ,product=p ,quantity=1)
        db.session.add(orderP)
        db.session.commit()
        data={
         'quantity': 3
        }
        resp = self.client.put('/order/1/product/1' ,data=json.dumps(data), content_type='application/json' )

        self.assert200(resp, "Falló el PUT")

        op=OrderProduct.query.all()[0]
        self.assertTrue(op.quantity == 3, "Fallo el PUT")
        
    def test_totalprice(self):
        p=Product(name="cuchara" ,price=25)
        orderP=OrderProduct(order_id=1, product_id=1 ,product=p ,quantity=1)
        
        self.assertTrue(orderP.totalPrice == 25, "Fallo la operacion totalPrice")


if __name__ == '__main__':
    unittest.main()

