from django.db import models


class ProposedItem:
    def __init__(self, color=None, img_path=None, goal=None, name=None):
        self.color = color 
        self.img_path = img_path 
        self.goal = goal
        self.name = name

class ItemPair:
    def __init__(self, first=None, second=None):
        self.first = first
        self.second = second

class TextureItem:
    def __init__(self, img_path=None, idx=None):
        self.img_path = img_path
        self.idx = idx


