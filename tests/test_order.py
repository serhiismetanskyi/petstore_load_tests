from locust import HttpUser, TaskSet, SequentialTaskSet, task, between

from data.order import NewOrder
from data.pet import NewPet
from utils.logger import Logger


class UserBehavior(TaskSet):

    @task
    class OrderTasks(SequentialTaskSet):
        pet_data = []
        pet_id = ""
        order_data = []
        order_id = ""
        order_status = ""
        order_complete = ""

        """ Create -> Get -> Delete """

        @task
        def order_create(self):
            """ Order Create """
            pet = NewPet()
            self.pet_data = pet.get_pet()
            self.pet_id = self.pet_data["id"]
            order = NewOrder(self.pet_id)
            self.order_data = order.get_order()
            self.order_id = self.order_data["id"]
            self.order_status = self.order_data["status"]
            self.order_complete = self.order_data["complete"]
            with self.client.post("/store/order", json=self.order_data, catch_response=True, name="Order Create") as response:
                task_result = ""
                Logger.add_request(test_name="Order Create", url="/store/order", method="POST", body=self.order_data)
                if response.status_code == 200:
                    task_result = f"{self.order_id} is created"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.order_id} create failed: Invalid Order"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.order_id} create failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def order_get_by_id(self):
            """ Get Order by ID """
            with self.client.get(f"/store/order/{self.order_id}", catch_response=True, name="Get Order by ID") as response:
                task_result = ""
                Logger.add_request(test_name="Get Order by ID", url=f"/store/order/{self.order_id}", method="GET")
                if response.status_code == 200:
                    order_id = response.json().get("id")
                    if order_id == self.order_id:
                        task_result = f"{self.order_id} is existed"
                        response.success()
                        print(task_result)
                    else:
                        task_result = f"{self.order_id} not found"
                        response.failure(task_result)
                        print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.order_id} get failed: Invalid ID supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.order_id} get failed: Order not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.order_id} is not exist: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def order_delete(self):
            """ Order Delete"""
            with self.client.delete(f"/store/order/{self.order_id}", catch_response=True, name="Order Delete") as response:
                task_result = ""
                Logger.add_request(test_name="Order Delete", url=f"/store/order/{self.order_id}", method="DELETE")
                if response.status_code == 200:
                    task_result = f"{self.order_id} is deleted"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.order_id} get failed: Invalid ID supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.order_id} get failed: Order not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.order_id} delete failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)


class OrderTestUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://petstore.swagger.io/v2"
    tasks = [UserBehavior]
