import sys

class Route:

  def __init__(self, locations, problem):
    self.locations = locations
    self.problem = problem
    # check the feasibility and compute the distance
    self.feasible = self.isFeasible()
    if self.feasible:
      self.distance = self.computeDistance()
    else:
      self.distance = sys.maxsize  # extremely large number
  
  def calculateServiceStartTime(self):
    curTime = 0
    for i in range(1, len(self.locations) - 1):
      prevNode = self.locations[i - 1]
      curNode = self.locations[i]
      dist = self.problem.distMatrix[prevNode.id][curNode.id]
      curTime = max(curNode.ready, curTime + prevNode.service + dist)
      self.locations[i].serviceStartTime = curTime
    
  def computeDiff(self, preNode, afterNode, insertNode):
    '''
    Method that calculates the cost of inserting a new node
    Parameters
    ----------
    preNode: Location
    afterNode: Location
    insertNode: Location
    '''
    return self.problem.distMatrix[preNode.id][insertNode.id] + self.problem.distMatrix[afterNode.id][
      insertNode.id] - self.problem.distMatrix[preNode.id][afterNode.id]

  # add this method
  def compute_cost_add_one_location(self, node_index, location):
    locationsCopy = self.locations.copy()
    locationsCopy.insert(node_index, location)
    # calculate the cost after inserting location
    cost = self.computeDiff(locationsCopy[node_index - 1], locationsCopy[node_index + 1], location)
    return cost
  
  def computeDistance(self):
    """
    Method that computes and returns the distance of the route
    """
    totDist = 0
    # for i in range(1, len(self.locations) - 1):
    for i in range(1, len(self.locations)):
      prevNode = self.locations[i - 1]
      curNode = self.locations[i]
      dist = self.problem.distMatrix[prevNode.id][curNode.id]
      totDist += dist
    return totDist
    
  def isFeasible(self):
    # route should start and end at the depot
    # route should start and end at the depot
    if self.locations[0] != self.problem.depot or self.locations[-1] != self.problem.depot:
      return False
    
    curTime = 0
    curLoad = 0
    curNode = self.locations[0]

    for i in range(1, len(self.locations) - 1):
      prevNode = self.locations[i - 1]
      curNode = self.locations[i]
      dist = self.problem.distMatrix[prevNode.id][curNode.id]
      # velocity = 1 dist = time
      curTime = max(curNode.ready, curTime + prevNode.service + dist)
      # check if time window is respected
      if curTime > curNode.due:
        return False
      # check if capacity not exceeded
      curLoad += curNode.demand
      if curLoad > self.problem.capacity:
        return False
    
    return True

  def removeLocation(self, location):
    """
    Method that removes a location from the route. 
    """

    self.locations.remove(location)
    # the distance changes, so update
    # revise.
    # self.distance = self.computeDistance(
    # *** add this method

  def addLocation(self, location, node_index):
    """
    Method that add a request to the route.
     """
    locationsCopy = self.locations.copy()
    locationsCopy.insert(node_index, location)
    afterInsertion = Route(locationsCopy, self.problem)
    if afterInsertion.feasible:
        self.locations.insert(node_index, location)
        cost = self.compute_cost_add_one_location(node_index, location)
        # revise.
        # self.distance = self.computeDistance()
        return cost
    else:
        return - 1
  
  def copy(self):
    """
    Method that returns a copy of the route
    """
    locationsCopy = self.locations.copy()
    return Route(locationsCopy, self.problem)

  def greedyInsert(self, location):
    """
    Method that inserts the pickup and delivery of a request at the positions
    that give the shortest total distance. Returns best route.
    Parameters
    ----------
    request : Request
        the request that should be inserted
    Returns
    -------
    bestInsert : Route
        Route with the best insertion
    """
    bestInsert = None  # if infeasible the bestInsert will be None
    minCost = sys.maxsize
    # iterate over all possible insertion positions for pickup and deliver
    for i in range(1, len(self.locations)):
      locationsCopy = self.locations.copy()
      locationsCopy.insert(i, location)
      afterInsertion = Route(locationsCopy, self.problem)
      # check if insertion is feasible
      if afterInsertion.feasible:
        # check if cheapest
        # revise. only calculate the cost
        cost = self.compute_cost_add_one_location(i, location)
        if cost < minCost:
          bestInsert = afterInsertion
          minCost = cost
    return bestInsert, minCost
  
  def print(self):
    """
    Method that prints the route
    """
    print("Route", end = '')
    for loc in self.locations:
      loc.print()
    print(" dist=" + str(self.distance))