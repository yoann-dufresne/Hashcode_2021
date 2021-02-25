class Car:
    def __init__(self, path):
        self.path = path
        self.state = False # T/F: moving/queued
        self.time = 0
        self.max_score = 0

class TrafficLight:
    def __init__(self, time):
        self.state = True # T/F: green/red
        self.time = time

class Intersection: # node
    def __init__(self, idx):
        self.idx = idx

class Street: # edge - maybe useless
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.queue = []
        self.tl = TrafficLight(0)

# the scheduling of a single intersection
class InterSchedule:
    def __init__(self, inter, streets, time):
        self.inter=inter # intersection ID
        self.streets=streets # list of streets in the order of the schedule
        # the following could be redundant
        self.time=time # list of times corresponding to the streets

