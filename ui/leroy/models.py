from django.db import models


class ProposedItem:
    def __init__(self, color=None, img_path=None, material=None):
        self.color= color 
        self.img_path = img_path 
        self.material = material


class TextureItem:
    def __init__(self, img_path=None, idx=None):
        self.img_path = img_path
        self.idx = idx


