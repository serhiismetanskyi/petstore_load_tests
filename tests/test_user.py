from locust import HttpUser, TaskSet, SequentialTaskSet, task, between

from data.user import NewUser
from utils.logger import Logger


class UserBehavior(TaskSet):

    @task
    class UserTasks(SequentialTaskSet):
        user_data = []
        user_data_for_update = []
        user_name = ""
        password = ""
        user_id = ""

        """ Registration -> Get -> Login -> Update -> Logout -> Delete """

        @task
        def user_registration(self):
            """ User Registration """
            user = NewUser()
            self.user_data = user.get_user()
            self.user_data_for_update = user.update_user_data()
            self.user_id = self.user_data["id"]
            self.user_name = self.user_data["username"]
            self.password = self.user_data["password"]
            with self.client.post("/user", json=self.user_data, catch_response=True,
                                  name="User Registration") as response:
                task_result = ""
                Logger.add_request(test_name="User Registration", url="/user", method="POST", body=self.user_data)
                if response.status_code == 200:
                    task_result = f"{self.user_name} is registered"
                    response.success()
                    print(task_result)
                else:
                    task_result = f"{self.user_name} registration failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def user_get(self):
            """ Get User """
            with self.client.get(f"/user/{self.user_name}", catch_response=True, name="Get User") as response:
                task_result = ""
                Logger.add_request(test_name="Get User", url=f"/user/{self.user_name}", method="GET")
                if response.status_code == 200:
                    user_id = response.json().get("id")
                    if user_id == self.user_id:
                        task_result = f"{self.user_name} is existed"
                        response.success()
                        print(task_result)
                    else:
                        task_result = f"{self.user_name} not found by {user_id}"
                        response.failure(task_result)
                        print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.user_name} get failed: Invalid username supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.user_name} get failed: User not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.user_name} is not exist: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def user_login(self):
            """ User Login """
            with self.client.get(f"/user/login?username={self.user_name}&password={self.password}", catch_response=True,
                                 name="User Login") as response:
                task_result = ""
                Logger.add_request(test_name="User Login",
                                   url=f"/user/login?username={self.user_name}&password={self.password}", method="GET")
                if response.status_code == 200:
                    task_result = f"{self.user_name} is authorized"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.user_name}: Invalid username/password supplied"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.user_name} login failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def user_update(self):
            """ User Update """
            with self.client.put(f"/user/{self.user_name}", json=self.user_data_for_update, catch_response=True,
                                 name="User Update") as response:
                task_result = ""
                Logger.add_request(test_name="User Update", url=f"/user/{self.user_name}", method="PUT",
                                   body=self.user_data_for_update)
                if response.status_code == 200:
                    task_result = f"{self.user_name} is updated"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.user_name} update failed: Invalid user supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.user_name} update failed: User not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.user_name} update failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def user_logout(self):
            """ User Logout """
            with self.client.get("/user/logout", catch_response=True, name="User Logout") as response:
                task_result = ""
                Logger.add_request(test_name="User Logout", url="/user/logout", method="GET")
                if response.status_code == 200:
                    task_result = f"{self.user_name} is logout"
                    response.success()
                    print(task_result)
                else:
                    task_result = f"{self.user_name} logout failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)

        @task
        def user_delete(self):
            """ User Deleted """
            with self.client.delete(f"/user/{self.user_name}", catch_response=True, name="User Delete") as response:
                task_result = ""
                Logger.add_request(test_name="User Delete", url=f"/user/{self.user_name}", method="DELETE")
                if response.status_code == 200:
                    task_result = f"{self.user_name} is deleted"
                    response.success()
                    print(task_result)
                elif response.status_code == 400:
                    task_result = f"{self.user_name} delete failed: Invalid username supplied"
                    response.failure(task_result)
                    print(task_result)
                elif response.status_code == 404:
                    task_result = f"{self.user_name} update failed: User not found"
                    response.failure(task_result)
                    print(task_result)
                else:
                    task_result = f"{self.user_name} update failed: Status code is {response.status_code}"
                    response.failure(task_result)
                    print(task_result)
                Logger.add_response(response, task_result)


class TestUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://petstore.swagger.io/v2"
    tasks = [UserBehavior]
