from locust import HttpUser, TaskSet, SequentialTaskSet, task, between

from data.pet import NewPet
from utils.logger import Logger


class UserBehavior(TaskSet):

    @task
    class PetTasks(SequentialTaskSet):
        pet_data = []
        pet_data_for_update = []
        pet_name = ""
        pet_id = ""
        pet_status = ""

        """ Create -> Update Image -> Get by ID -> Update by ID -> Delete """

        @task
        def pet_create(self):
            """ Pet Create """
            pet = NewPet()
            self.pet_data = pet.get_pet()
            self.pet_data_for_update = pet.update_pet_data()
            self.pet_id = self.pet_data["id"]
            self.pet_name = self.pet_data["name"]
            self.pet_status = self.pet_data["status"]
            with self.client.post("/pet", json=self.pet_data, catch_response=True, name="Pet Create") as response:
                task_result = ""
                Logger.add_request(test_name="Pet Create", url="/pet", method="POST", body=self.pet_data)
                if response.status_code == 200:
                    task_result = f"{self.pet_name} is created"
                    response.success()
                    print(task_result)
                elif response.status_code == 405:
                    task_result = f"{self.pet_name} create failed: Invalid input"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.pet_name} create failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task(1)
        def pet_update_img(self):
            """ Pet Image Update """
            data = {"additionalMetadata": "New Pet Image"}
            files = {'file': open('./data/pet_img.jpg', 'rb')}
            with self.client.post(f"/pet/{self.pet_id}/uploadImage", data=data, files=files, catch_response=True, name="Pet Image Update") as response:
                task_result = ""
                Logger.add_request(test_name="Pet Image Update", url=f"/pet/{self.pet_id}/uploadImage", method="POST")
                if response.status_code == 200:
                    task_result = f"{self.pet_name} image is updated"
                    response.success()
                    print(task_result)
                else:
                    task_result = f"{self.pet_name} image update failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task(10)
        def pet_get_by_id(self):
            """ Get Pet by ID """
            with self.client.get(f"/pet/{self.pet_id}", catch_response=True, name="Get Pet by ID") as response:
                task_result = ""
                Logger.add_request(test_name="Get Pet by ID", url=f"/pet/{self.pet_id}", method="GET")
                if response.status_code == 200:
                    pet_id = response.json().get("id")
                    if pet_id == self.pet_id:
                        task_result = f"{self.pet_name} is existed"
                        response.success()
                        print(task_result)
                    else:
                        task_result = f"{self.pet_name} not found by {pet_id}"
                        response.failure(task_result)
                        print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.pet_name} get failed: Invalid ID supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.pet_name} get failed: Pet not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.pet_name} is not exist: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)


        @task
        def pet_update_by_id(self):
            """ Pet Update by ID"""
            with self.client.post(f"/pet/{self.pet_id}", data=self.pet_data_for_update, catch_response=True, name="Pet Update by ID") as response:
                task_result = ""
                Logger.add_request(test_name="Pet Update by ID", url=f"/pet/{self.pet_id}", method="POST", body=self.pet_data_for_update)
                if response.status_code == 200:
                    task_result = f"{self.pet_name} is updated"
                    response.success()
                    print(task_result)
                elif response.status_code == 405:
                    task_result = f"{self.pet_name} update failed: Invalid input"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.pet_name} update failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def pet_delete(self):
            """ Pet Delete"""
            headers = {"api_key": "special-key"}
            with self.client.delete(f"/pet/{self.pet_id}", headers=headers, catch_response=True, name="Pet Delete") as response:
                task_result = ""
                Logger.add_request(test_name="Pet Delete", url=f"/pet/{self.pet_id}", method="DELETE")
                if response.status_code == 200:
                    task_result = f"{self.pet_name} is deleted"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.pet_name} delete failed: Invalid ID supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.pet_name} delete failed: Pet not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.pet_name} delete failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)


class PetTestUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://petstore.swagger.io/v2"
    tasks = [UserBehavior]
