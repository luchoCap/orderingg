from sqlalchemy import and_

from app import app, db
from app.models import Product, Order, OrderProduct
from flask import request, jsonify, render_template

@app.route("/")
def hello():
    return render_template('orders.html')

@app.route("/product", methods=['GET', 'POST'])
def products():
    """
    Endpoint para obtener todos los productos o crear uno nuevo
    :return:
    """
    if request.method == 'POST':
        # Crea un nuevo producto recibiendo un JSON con atributos name y price
        # Ejemplo: {'name': 'Tenedor', 'price': 50}
        p = Product(name=request.get_json()['name'], price=request.get_json()['price'])
        db.session.add(p)
        db.session.commit()
        return jsonify(p.serialize)
    else:
        # Obtiene todos los productos disponibles
        p = Product.query.all()
        return jsonify([i.serialize for i in p])

@app.route("/order", methods=['GET'])
def orders():
    """
    Obtiene todas las ordenes
    """

    orders = Order.query.all()
    return jsonify([order.serialize for order in orders])

@app.route("/order/<pk>", methods=['GET'])
def order(pk):
    """
    Obtiene la orden con id `pk`

    Si no se encuentra la orden, se responde con un 404
    """

    # obtenemos las ordenes
    order = Order.query.get(pk)

    # Si la orden no existe, levantamos el error
    if (not order):
        return jsonify({ 'error': 'not-found' }), 404

    return jsonify(order.serialize)

@app.route("/order/<pk>/product", methods=['POST'])
def addProductToOrder(pk):
    # obtenemos las ordenes
    order = Order.query.get(pk)

    # Si la orden no existe, levantamos el error
    if (not order):
        return jsonify({ 'error': '<order {}> not found'.format(pk) }), 404

    product_data = request.get_json()
    product = product_data['product']

    product_exists = any([
        p.product.id == product['id'] for p in order.products
    ])

    # Si el producto existe en la orden levantamos el error
    if (product_exists):
        return jsonify({
            'error': '<product {}> exists in <order {}>. Use PUT method'
                .format(product['id'], pk)
        }), 400

    orderProduct = OrderProduct(quantity=product_data['quantity'])
    orderProduct.product = Product.query.get(product['id'])
    order.products.append(orderProduct)

    db.session.add(order)
    db.session.commit()

    return jsonify(order.serialize), 201

@app.route("/order/<pk_order>/product/<pk_product>", methods=['GET', 'PUT'])
def order_product_detail(pk_order, pk_product):
    """
    Obtiene un producto de una orden y modifica un producto de una orden

    Si no se encuentra la orden, se responde con un 404.
    Si no se encuentra el producto, se responde con un 404
    """

    order_product = OrderProduct.query.filter(and_(OrderProduct.order_id==pk_order, OrderProduct.product_id==pk_product)).all()[0]

    if (not order_product):
        return jsonify({ 'error': 'not-found' }), 404

    if request.method == 'GET':
        return jsonify(order_product.serialize)
    else:
        new_quantity = request.get_json()['quantity']
        new_product = request.get_json()['product']

        if (new_quantity):
            order_product.quantity = new_quantity
        if (new_product):
            order_product.product = Product.query.get(new_product)
            order = Order.query.get(pk_order)
            order.products.append(order_product)
        db.session.commit()
        return jsonify(order_product.serialize)
