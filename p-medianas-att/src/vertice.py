import random
import uuid


class Vertice(object):
    def __init__(self, x, y, cap, demand):
        self.x = x
        self.y = y
        self.cap = cap - demand
        self.capReal = cap - demand
        self.demand = demand
        self.id = uuid.uuid4()

    def distance(self, x, y): return ((self.x-x)**2 + (self.y-y)**2)**0.5
