import numpy as np
from location import Location

class VRPTW:
  def __init__(self, name, locations, depot, vehicleCapacity):
    self.name = name
    self.locations = locations
    self.depot = depot
    self.capacity = vehicleCapacity
    self.distMatrix = np.zeros((len(self.locations), len(self.locations)))
    for i in self.locations:
      for j in self.locations:
        distItoJ = Location.getDistance(i, j)
        self.distMatrix[i.id, j.id] = distItoJ
  
  def readInstance(fileName):
    f = open(fileName)
    locations = list()
    depot = None
    serviceStartTime = 0
    for line in f.readlines()[8:]:
      asList = []
      n = 16
      for index in range (0, len(line), n):
        asList.append(line[index:index + n].strip())
      lid = int(asList[0])
      x = int(asList[1])
      y = int(asList[2])
      demand = int(asList[3])
      ready = int(asList[4])
      due = int(asList[5])
      service = int(asList[6])
      if (lid == 0):
        depot = Location(lid, x, y, demand, ready, due, service, serviceStartTime)
      location = Location(lid, x, y, demand, ready, due, service, serviceStartTime)
      locations.append(location)
    f = open(fileName)
    capLine = f.readlines()[4]
    capacity = int(capLine[10:20].strip())
    return VRPTW(fileName, locations, depot, capacity)
      