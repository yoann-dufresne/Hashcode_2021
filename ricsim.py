#!/usr/bin/env python3

import copy
from collections import defaultdict,deque

from model import * 


class RicSim:
    def __init__(self,intersections,street_map,cars,F):
        # input
        self.bonus = F # fixed bonus points for a car completing its path
        self.street_map = street_map # dict: street_name -> (B,E,street_name,L)
        self.intersections = intersections # dict: intersection_id -> (input_street_names,output_street_names)
        self.cars = copy.deepcopy(cars) # list of Car objects
        # simulation data structures / variables
        self.duration = 0 # duration of the simulation
        self.scheduling = {} # dict: intersection_id -> list of (street_name,traffic_light_time)
        self.active_street = {} # dict: intersection_id -> (index of which street has green light, time left)
        self.score = 0 # accumulated score
        self.elapsed = 0 # time passed since the beginning of simulation
        self.street_queue = {} # dict: street_name -> cars in queue
        self.moving_cars = {} # dict: street_name -> cars still moving along the street

    #scheduling: dictionary intersection -> list of InterSchedule
    def simulate(self,cycles,duration):
        #print(f'started simulation')
        self.sim_init(cycles,duration)
        while self.elapsed < self.duration:
            self.cross_intersections()
            self.move_cars()
            self.elapsed+=1
        return self.score

    def sim_init(self,cycles,duration):
        #print(f'simulation initialization')
        self.duration = duration
        self.scheduling = cycles
        self.score = 0
        self.elapsed = 0
        self.street_queue = defaultdict(deque)
        self.moving_cars = defaultdict(deque)
        # initialize remaining time for the first (scheduled) traffic light in each intersection
        for inter,in_streets in self.scheduling.items():
            if len(in_streets)>0:
                street_name,street_time = in_streets[0]
                self.active_street[inter]=(0,street_time)
                #print(f'intersection {inter} -> {street_name},{street_time} -- {in_streets}')
        # put cars at the end of their first street
        for car in self.cars:
            car.path = deque(car.path)
            if len(car.path) > 0:
                street,_=car.path.popleft()
                self.street_queue[street].append(car)
                #print(f'Car({":".join(x for x,_ in car.path)}) put in queue at {street}')

    # let cars cross green-light intersections
    # advances time for traffic lights
    def cross_intersections(self):
        for inter,in_streets in self.scheduling.items():
            # let a car (if it exists) pass the active street of the intersection
            active_i,active_time = self.active_street[inter]
            active_street,active_maxtime = in_streets[active_i]
            #print(f't={self.elapsed}: inter={inter} active={active_i+1}/{len(in_streets)}:{active_street}({active_time}/{active_maxtime}) queue={ self.street_queue[active_street] }')
            if len(self.street_queue[active_street])>0:
                car = self.street_queue[active_street].popleft()
                car.time = 0
                out_street,_ = car.path.popleft()
                self.moving_cars[out_street].append(car)
                #print(f'Car({":".join(x for x,_ in car.path)}) passes intersection {inter} and enters {out_street} at time {self.elapsed+1}/{self.duration}')
            # update remaining time of the active street
            # if it reaches 0 -> set the next scheduled street
            active_time-=1
            if active_time == 0:
                active_i = (active_i+1)%len(in_streets)
                active_street,active_maxtime=in_streets[active_i]
                self.active_street[inter]=(active_i,active_maxtime)
                continue
            self.active_street[inter]=(active_i,active_time)

    def move_cars(self):
        # advances cars entering or already moving along a street
        for street,moving_cars in self.moving_cars.items():
            street_time = self.street_map[street][3]
            if len(moving_cars)>0:
                car = moving_cars[0]
                if car.time+1 == street_time: # car arrived at the end of street
                    moving_cars.popleft()
                    if len(car.path) == 0: # car finished its journey, do not queue it up, update score
                        self.score += self.bonus + self.duration - (self.elapsed+1)
                    else:
                        self.street_queue[street].append(car)
            for car in moving_cars:
                car.time+=1



