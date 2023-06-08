import datetime
import time
from random import randint

from data.test_data import OrderTestData

""" Test Data for Pet """


class NewOrder(OrderTestData):

    def __init__(self, petId):
        self.id = int(time.time() * 1000)
        self.petId = petId
        self.quantity = randint(1, 5)
        self.shipDate = str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        self.status = OrderTestData.get_order_status()
        self.complete = "false"

    def get_order(self):
        order_data = {
            "id": self.id,
            "petId": self.petId,
            "quantity": self.quantity,
            "shipDate": self.shipDate,
            "status": self.status,
            "complete": self.complete
        }
        return order_data

    def update_order_data(self):
        self.complete = "true"
        order_data_for_update = {
            "complete": self.complete
        }
        return order_data_for_update