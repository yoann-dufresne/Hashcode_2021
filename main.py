#!/usr/bin/env python3

import sys
import glob
import os
import random

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
def parse(filename):
    lines = open(filename).readlines()
    global D,I,S,V,F
    D,I,S,V,F = map(int,lines[0].split())
   
    global streets
    streets = []
    for line in lines[1:S+1]:
        assert(len(line.split()) == 4)
        B,E, name, L = line.split()
        B,E,L=map(int,[B,E,L])
        streets += [(B,E,name,L)]
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
    for line in lines[S+1:]:
        P = int(line.split()[0])
        assert(len(line.split()) == P+1)
        paths += [line.split()[1:]]
    assert(len(paths) == V)
parse(sys.argv[1])



# smart things

class Solution:

  def __init__(self):
    self.score = 0
    self.best_score = 0

    self.cycles = {}

  def get_score(self):
    return self.score

  def save(self):
    global overall_best_score

    if self.get_score() >= overall_best_score:
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


def greedy_cars




def main():
  sol = naive_solution()
  sol.save()

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
