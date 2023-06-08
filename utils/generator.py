from faker import Faker

""" Fake Data Generator """


class DataGenerator:

    def __init__(self, seed=None):
        self.fake = Faker()
        if seed:
            self.fake.seed(seed)

    def first_name(self):
        return self.fake.first_name()

    def last_name(self):
        return self.fake.last_name()

    def phone_number(self):
        return self.fake.phone_number()