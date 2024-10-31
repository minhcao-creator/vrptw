import math

class Location:
  def __init__(self, id, x, y, demand, ready, due, service, serviceStartTime):
    self.id = id
    self.x = x
    self.y = y
    self.demand = demand
    self.ready = ready
    self.due = due
    self.service = service
    self.serviceStartTime = serviceStartTime
  
  def getDistance(l1, l2):
    dx = l1.x - l2.x
    dy = l1.y - l2.y
    return round(math.sqrt(dx ** 2 + dy ** 2))