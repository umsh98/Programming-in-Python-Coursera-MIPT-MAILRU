import os
import csv


class CarBase:

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = self.is_valid_value(brand)
        self.photo_file_name = self.is_valid_filename(photo_file_name)
        self.carrying = float(self.is_valid_value(carrying))

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    @staticmethod
    def is_valid_filename(filename):
        valid_ext = ['.jpg', '.jpeg', '.png', '.gif']
        _, ext = os.path.splitext(filename)
        if ext in valid_ext:
            return filename
        else:
            raise ValueError

    @staticmethod
    def is_valid_value(value):
        if value == '':
            raise ValueError
        return value


class Car(CarBase):

    required_param = ['brand', 'photo_file_name', 'carrying',
                      'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.is_valid_value(passenger_seats_count))
        self.car_type = 'car'


class Truck(CarBase):

    required_param = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        try:
            body_length, body_width, body_height = body_whl.split('x')
            body_length = float(body_length)
            body_width = float(body_width)
            body_height = float(body_height)
        except ValueError:
            self.body_length = 0.0
            self.body_width = 0.0
            self.body_height = 0.0
        else:
            self.body_length = body_length
            self.body_width = body_width
            self.body_height = body_height

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):

    required_param = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.is_valid_value(extra)
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):

    technic_param = ['car_type', 'brand', 'passenger_seats_count',
                     'photo_file_name', 'body_whl', 'carrying', 'extra']
    technic_classes = {'car': Car, 'truck': Truck, 'spec_machine': SpecMachine}
    car_list = []
    with open(csv_filename) as f:
        data = csv.reader(f, delimiter=';')
        next(data)
        for line in data:
            technic = {a: b for a, b in zip(technic_param, line)}
            try:
                car_class = technic_classes[technic['car_type']]
                car_params = [technic[param] for param in car_class.required_param]
                car_list.append(car_class(*car_params))
            except Exception:
                pass
    return car_list
