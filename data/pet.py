import time

from data.test_data import PetTestData

""" Test Data for Pet """


class NewPet(PetTestData):

    def __init__(self):

        self.category = PetTestData.get_pet_category()
        self.tag = PetTestData.get_pet_tag()

        self.id = int(time.time() * 1000)
        self.category_id = self.category["id"]
        self.category_name = self.category["name"]
        self.name = PetTestData.get_pet_name()
        self.photoUrls = "string"
        self.tag_id = self.tag["id"]
        self.tag_name = self.tag["name"]
        self.status = PetTestData.get_pet_status()

    def get_pet(self):
        pet_data = {
              "id": self.id,
              "category": {
                "id": self.category_id,
                "name": self.category_name
              },
              "name": self.name,
              "photoUrls": [
                self.photoUrls
              ],
              "tags": [
                {
                  "id": self.tag_id,
                  "name": self.tag_name
                }
              ],
              "status": self.status
            }
        return pet_data

    def update_pet_data(self):
        self.status = PetTestData.get_pet_status()
        self.name = PetTestData.get_pet_name()
        pet_data_for_update = {
            "name": self.name,
            "status": self.status
        }
        return pet_data_for_update