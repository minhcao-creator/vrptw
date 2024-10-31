import sys
from route import Route

class Repair:

  def __init__(self, problem, solution):
    self.problem = problem
    self.solution = solution
  
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

  def findRegretInsertion(self):
    '''
    Method that finds the insertion to maximize regret value
    Returns
    -------
    [request, route, prevNode_index, afterNode_index]
    '''
    maxRegret = -1
    insertRoute = None
    insertLocation = None
    node_index = -1
    maxCost = sys.maxsize  # extremely large number
    for location in self.solution.notServed:
      tempCost = []
      inserted = False
      # print('new request----------')
      # print(request)
      for route in self.solution.routes:
        locationsCopy = route.locations.copy()
        for i in range(1, len(route.locations)):
          cost = route.compute_cost_add_one_location(i, location)
          locationsCopy.insert(i, location)
          afterInsertion = Route(locationsCopy, self.problem)
          if afterInsertion == None:
            continue
          # check if insertion is feasible
          if afterInsertion.feasible:
            inserted = True
            tempCost.append([cost, route, i])
      # if we have only one feasible insertion
      if len(tempCost) == 1:
        locList = [self.problem.depot, location, self.problem.depot]
        newRoute = Route(locList, self.problem)
        diff = newRoute.distance
        tempCost.append([diff, None, 0])
      # if we were not able to insert, create a new route
      if not inserted:
        # print('not insert')
        # create a new route with the request
        locList = [self.problem.depot, location, self.problem.depot]
        newRoute = Route(locList, self.problem)
        diff = newRoute.distance
        tempCost.append([diff, None, 0])
      tempCost = sorted(tempCost, key = lambda d: d[0], reverse = False)
      # print('sorted tempCost')
      # print(tempCost)
      if len(tempCost) > 1 and (tempCost[1][0] - tempCost[0][0]) > maxRegret:
        maxRegret = tempCost[1][0] - tempCost[0][0]
        # print('maxRegret',maxRegret)
        insertRoute = tempCost[0][1]
        insertLocation = location
        node_index = tempCost[0][2]
      # all request can only be inserted into a new route, choose greedy insertion to minimize the cost
      elif len(tempCost) == 1 and (maxRegret <= 0) and tempCost[0][0] < maxCost:
        maxRegret = 0
        maxCost = tempCost[0][0]
        insertRoute = tempCost[0][1]
        insertLocation = location
        node_index = tempCost[0][2]
    return insertLocation, insertRoute, node_index

  def executeRegretInsertion(self):
    """
    Method that inserts the unserved request with the largest regret first in the solution

    This is repair method number 2 in the ALNS

    """
    while len(self.solution.notServed) > 0:
      insertRequest, insertRoute, node_index, = self.findRegretInsertion()
      # print(insertRequest, insertRoute, preNode_index, afterNode_index)
      self.solution.addLocation(insertRequest, insertRoute, node_index)
      # for route in self.solution.routes:
      #     route.print()
    
  def executeGreedyInsertion(self):
    """
    Method that greedily inserts the unserved requests in the solution

    This is repair method number 1 in the ALNS

    """

    while len(self.solution.notServed) > 0:
      for loc in self.solution.notServed:
        inserted = False
        minCost = sys.maxsize  # initialize as extremely large number
        bestInsert = None  # if infeasible the bestInsert will be None
        for route in self.solution.routes:
          afterInsertion, cost = route.greedyInsert(loc)
          if afterInsertion == None:
            continue
          if cost < minCost:
            inserted = True
            removedRoute = route
            bestInsert = afterInsertion
            minCost = cost
        # if we were not able to insert, create a new route
        if not inserted:
          # create a new route with the request
          locList = [self.problem.depot, loc, self.problem.depot]
          newRoute = Route(locList, self.problem)
          self.solution.routes.append(newRoute)
          self.solution.distance += newRoute.distance
        else:
          self.solution.routes.remove(removedRoute)
          self.solution.routes.append(bestInsert)
          self.solution.distance += minCost
        # update the lists with served and notServed requests
        self.solution.served.append(loc)
        self.solution.notServed.remove(loc)
    
  def executeRandomInsertion(self, randomGen):
      """
      Method that randomly inserts the unserved requests in the solution

      This is repair method number 0 in the ALNS

      Parameters
      ----------
      randomGen : Random
          Used to generate random numbers

      """

      # iterate over the list with unserved requests
      while len(self.solution.notServed) > 0:
        # pick a random request
        loc = randomGen.choice(self.solution.notServed)
        # keep track of routes in which req could be inserted
        potentialRoutes = self.solution.routes.copy()
        inserted = False
        while len(potentialRoutes) > 0:
          # pick a random route
          randomRoute = randomGen.choice(potentialRoutes)
          afterInsertion, cost = randomRoute.greedyInsert(loc)
          if afterInsertion == None:
            # insertion not feasible, remove route from potential routes
            potentialRoutes.remove(randomRoute)
          else:
            # insertion feasible, update routes and break from while loop
            inserted = True
            # print("Possible")
            self.solution.routes.remove(randomRoute)
            self.solution.routes.append(afterInsertion)
            self.solution.distance += cost
            break
        # if we were not able to insert, create a new route
        if not inserted:
          # create a new route with the request
          locList = [self.problem.depot, loc, self.problem.depot]
          newRoute = Route(locList, self.problem)
          self.solution.routes.append(newRoute)
          self.solution.distance += newRoute.distance
        # update the lists with served and notServed requests
        self.solution.served.append(loc)
        self.solution.notServed.remove(loc)