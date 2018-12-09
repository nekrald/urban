from django.db import models


class Item:

    def __init__(self):
        self.price = None
        self.color = None
        self.img_path = None
        self.material = None

    def __init__(self, price, color, img_path, material):
        self.price = price 
        self.color= color 
        self.img_path = img_path 
        self.material = material


