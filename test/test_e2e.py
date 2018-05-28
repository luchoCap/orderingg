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

#  def test_title(self):
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

