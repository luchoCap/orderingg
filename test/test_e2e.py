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

      #def test_title(self):

       # orden = Order()
        #db.session.add(orden)
        #producto = Product(name= 'Cuchara', price= 20)
        #db.session.add(producto)
        #db.session.commit()
        #driver = self.driver
        #driver.get(self.baseURL)
        #add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        #add_product_button.click()
        #modal = driver.find_element_by_id('modal')
        #assert modal.is_displayed(), "El modal no esta visible"
    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

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
        selected_box=driver.find_element_by_xpath('//*[@id="select-prod"]/option[1]')

        quantity_box = driver.find_element_by_xpath('//*[@id="quantity"]')
        totalprice_box=driver.find_element_by_id("total-price")
        nombre_box=driver.find_element_by_id("nombre")
        time.sleep(1)

        self.assertNotEquals(selected_box," ")
        self.assertNotEquals(nombre_box," ")
        self.assertNotEquals(quantity_box," ")
        self.assertNotEquals(totalprice_box," ")

    



if __name__ == "__main__":
    unittest.main()

