import random

from utils.generator import DataGenerator

""" Test Data """


class UserTestData:

    @staticmethod
    def get_first_name():
        generator = DataGenerator()
        first_name = generator.first_name()
        return first_name

    @staticmethod
    def get_last_name():
        generator = DataGenerator()
        last_name = generator.last_name()
        return last_name

    @staticmethod
    def get_phone_number():
        generator = DataGenerator()
        phone_number = generator.phone_number()
        return phone_number


class PetTestData:

    @staticmethod
    def get_pet_name():
        generator = DataGenerator()
        first_name = generator.first_name()
        return first_name

    @staticmethod
    def get_pet_category():
        data = {
            "01": "Cats",
            "02": "Dogs"
        }
        random_category_id = random.choice(list(data.keys()))
        random_category_name = data[random_category_id]
        random_data = (("id", random_category_id), ("name", random_category_name))
        random_category = dict(random_data)
        return random_category

    @staticmethod
    def get_pet_tag():
        data = {
            "01": "Big",
            "02": "Small",
            "03": "Shaggy",
            "04": "Smooth-haired"
        }
        random_tag_id = random.choice(list(data.keys()))
        random_tag_name = data[random_tag_id]
        random_data = (("id", random_tag_id), ("name", random_tag_name))
        random_tag = dict(random_data)
        return random_tag

    @staticmethod
    def get_pet_status():
        data = {"available", "pending", "sold"}
        random_status = random.choice(list(data))
        return random_status


class OrderTestData:

    @staticmethod
    def get_order_status():
        data = {"placed", "approved", "delivered"}
        random_status = random.choice(list(data))
        return random_status
