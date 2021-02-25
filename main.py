#!/usr/bin/env python3

import sys
import glob
import os
import random
import networkx as nx
from collections import defaultdict
from copy import deepcopy
from model import *


overall_best_score = 0

def look_for_best_score():
  global overall_best_score

  infile = sys.argv[1]
  directory = os.path.dirname(infile)
  file_list = glob.glob(infile + "*_.out")

  for file in file_list:
    file_score = int(file.split("_")[-2])
    if file_score > overall_best_score:
      overall_best_score = file_score


# parsing
D, I, S, V, F = 0, 0, 0, 0, 0
streets = []
paths = []
intersections = {}
street_map = {}
cars = []
def parse(filename):
    lines = open(filename).readlines()
    global D,I,S,V,F
    D,I,S,V,F = map(int,lines[0].split())
   
    global streets, street_map
    streets = []
    street_map = {}
    for line in lines[1:S+1]:
        assert(len(line.split()) == 4)
        B,E, name, L = line.split()
        B,E,L=map(int,[B,E,L])
        streets += [(B,E,name,L)]
        street_map[name] = (B,E,name,L)
    assert(len(streets) == S)

    global intersections
    for B, E, name, _ in streets:
      if B not in intersections:
        intersections[B] = [], []
      intersections[B][1].append(name)

      if E not in intersections:
        intersections[E] = [], []
      intersections[E][0].append(name)

       
    global paths
    global cars
    for line in lines[S+1:]:
        P = int(line.split()[0])
        assert(len(line.split()) == P+1)
        paths += [[(s, street_map[s][3]) for s in line.strip().split()[1:]]]
        cars.append(Car(paths[-1]))
    assert(len(paths) == V)
parse(sys.argv[1])



# smart things

class Solution:

  def __init__(self):
    self.score = 0
    self.best_score = 0

    self.cycles = {}

  def get_score(self,verbose=False):
    # gather queue at each street extremity
    street_lqueue = defaultdict(list)
    lights = defaultdict()
    cars_copy = deepcopy(cars)
    # make all cars be at the extremity of their street to start sim
    for car in cars_copy:
        car.street = car.path[0][0]
        car.time = car.path[0][1]
        street_lqueue[car.street] += [car]
    # set the light pattern
    cycles = defaultdict()
    cycles_lens = defaultdict()
    for i in self.cycles:
        time = 0
        cycle_len = sum([d for s,d in self.cycles[i]])
        for street, duration in self.cycles[i]:
            cycles_lens[street] = cycle_len
            cycles[street] = [False] * cycle_len
            for _ in range(duration):
                cycles[street][time] = True
                time += 1
    def is_light_on(street,T):
        cycle_len = cycles_lens[street]
        cycle = cycles[street]
        pos = T % cycle_len
        return cycle[pos]
    # now advance cars whenever possible
    score = 0
    for T in range(D):
        if verbose:
            print("T=",T)
        for car in cars_copy:
            if car.done: continue
            street = car.street
            #print(street)
            # move the car
            car.time += 1
            # add car to street queue if its time has come
            L = street_map[street][3]
            if car.time == L:
                street_lqueue[street] += [car]
            # see if it is waiting for the light
            if len(street_lqueue[street]) > 0 and car == street_lqueue[street][0]:
                # move car to next street, if possible, otherwise it waits
                if is_light_on(street,T):
                    street_lqueue[street] = street_lqueue[street][1:]
                    #print("path",car.path)
                    if len(car.path) == 1:
                        # car is done! add to score
                        if verbose:
                            print("car is done!",score)
                        car.done = True
                        score += F + D - T
                    else:
                        new_street = car.path[1][0]
                        #print("moving car from",street,"to",new_street)
                        car.path = car.path[1:] # modifies the car path..
                        car.street = car.path[0][0]
                        car.time = 0
    return score
            


  def save(self):
    global overall_best_score

    if self.get_score(verbose=True) >= overall_best_score:
      print("saved", self.get_score())
      with open(sys.argv[1] + "_" + str(self.get_score()) + "_.out", "w") as fp:
        print(len(self.cycles), file=fp)
        for i, cycle in self.cycles.items():
          print(i, file=fp)
          print(len(cycle), file=fp)
          for street, time in cycle:
            print(street, time, file=fp)
    else:
      print("not saved", self.get_score())



def naive_solution():
  global intersections
  sol = Solution()

  for i, tup in intersections.items():
    sol.cycles[i] = [(x, 1) for x in tup[0]]

  # print(sol.cycles)
  return sol


def greedy_cars():
  global cars, street_map, intersections

  # Compute hot points
  busyness = {s:0 for s in street_map.keys()}
  for car in cars:
    for street, _ in car.path:
      busyness[street] += 1

  # For each intersection determine the cycle regarding the busyness
  sol = Solution()
  for i, tup in intersections.items():
    inputs = tup[0]
    local_busy = [busyness[street] for street in inputs if busyness[street] > 0]
    # print(local_busy)
    if len(local_busy) == 0:
      continue

    busy_min = min(local_busy)
    sol.cycles[i] = [(street, round(busyness[street]/busy_min)) for street in inputs if busyness[street] > 0]
    #print(sol.cycles[i])

  return sol


def main():
  greedy_cars()
  sol = greedy_cars()
  sol.save()
  # exit(0)

  # Store cars
  cars = []
  for path in paths:
    cars.append(Car(path))

  # Store graph
  G = nx.DiGraph()
  # Nodes:
  for inter_idx in set(street[0] for street in streets) | set(street[1] for street in streets):
    G.add_node(inter_idx, data = Intersection(inter_idx))
  # Edges:
  for sinter, einter, name, length in streets:
    G.add_edge(sinter, einter, data = Street(name, length))






if __name__ == "__main__":
  look_for_best_score()
  main()
