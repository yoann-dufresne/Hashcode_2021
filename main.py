#!/usr/bin/env python3

import sys
import glob
import os
import random



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



class Solution:

  def __init__(self):
    self.score = 0
    self.best_score = 0

  def get_score(self):
    return self.score

  def save(self):
    global overall_best_score

    if self.get_score() >= overall_best_score:
      print("saved", self.get_score())
      with open(sys.argv[1] + "_" + str(self.get_score()) + "_.out", "w") as fp:
        print("solution content", file=fp)
    else:
      print("not saved", self.get_score())



def naive_solution():
  sol = Solution()
  sol.score = random.randint(0, 100)

  return sol




def main():
  sol = naive_solution()
  sol.save()







if __name__ == "__main__":
  look_for_best_score()
  main()
