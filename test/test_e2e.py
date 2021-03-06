import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

from werkzeug.serving import make_server

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.t = threading.Thread(target=self.app.run)
        self.t.start()

        time.sleep(1)

        self.driver = webdriver.Chrome()

#    def test_title(self):
 #       driver = self.driver
  #      driver.get(self.baseURL)
   #     add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
    #    add_product_button.click()
     #   modal = driver.find_element_by_id('modal')
      #  assert modal.is_displayed(), "El modal no esta visible"


    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

    def test_borrar_fila(self):
        #Creo los productos
        prod = Product( name= 'Tenedor', price= 50)
        db.session.add(prod)
        prod2 = Product( name= 'Calabaza', price= 30)
        db.session.add(prod2)

        #Creo una orden
        order = Order()
        db.session.add(order)

        #Añado los productos a la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= prod)
        db.session.add(orderProduct)
        orderProduct = OrderProduct(order_id= 1, product_id= 2, quantity= 1, product= prod2)
        db.session.add(orderProduct)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)

        time.sleep(1)

        delete_product_button = driver.find_element_by_xpath('//*[@id="orders"]/table/tbody/tr[1]/td[6]/button[2]')
        delete_product_button.click()

        time.sleep(1)

        op = OrderProduct.query.all()

        # Verifica que se haya borrado el producto de la lista de productos
        self.assertEqual(len(op), 1, "No se borró el producto")

        #Verifica que se haya borrado el producto correcto
        self.assertNotEqual(op[0].product, prod, "No se borró el producto correcto")
        
    def test_modal(self):
        orden = Order()
        db.session.add(orden)
        producto = Product(name= 'Cuchara', price= 20)
        db.session.add(producto)
        orderP=OrderProduct(order_id=1, product_id=1 ,product=producto ,quantity=1)
        db.session.add(orderP)
        db.session.commit()
       
        driver = self.driver
        driver.get(self.baseURL)
        submit_buttom=driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[1]')
        submit_buttom.click()

        selected_box=driver.find_element_by_id('select-prod').text
        quantity_box = driver.find_element_by_id('quantity').text
        totalprice_box=driver.find_element_by_id('total-price').text
        nombre_box=driver.find_element_by_id('nombre').text

        self.assertNotEqual(selected_box," ")
        self.assertNotEqual(nombre_box," ")
        self.assertNotEqual(quantity_box," ")
        self.assertNotEqual(totalprice_box," ")

    def test_integracion_cantidad_negativa(self):
        orde = Order(id=1)
        db.session.add(orde)

        prod = Product(id=1, name='Silla', price= 30)
        db.session.add(prod)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)

        boton_agregar_prod = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        boton_agregar_prod.click()

        select = driver.find_element_by_xpath('//*[@id="select-prod"]')
        select.click()
        
        opc = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
        opc.click()


        cant_ingresada = driver.find_element_by_xpath('//*[@id="quantity"]')
        cant_ingresada.send_keys("-10")

        boton_guardar = driver.find_element_by_xpath('//*[@id="save-button"]')
        time.sleep(2)
        boton_guardar.click()


    

    

    




if __name__ == "__main__":
    unittest.main()
