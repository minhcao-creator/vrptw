from route import Route

class Solution:

  def __init__(self, problem, routes, served, notServed):
    self.problem = problem
    self.routes = routes
    self.served = served
    self.notServed = notServed
    self.distance = self.computeDistance()
  
  def computeDistance(self):
    """
    Method that computes the distance of the solution
    """
    self.distance = 0
    for route in self.routes:
      self.distance += route.distance
    return self.distance
  
  def computeDistanceWithNoise(self, max_arc_dist, noise, randomGen):
    """
    Method that computes the distance of the solution and implements noise
    """
    self.noise_succesful = 1
    self.no_noise_succesful = 1
    self.normal_distance = 0
    for route in self.routes:
      self.normal_distance += route.distance
    maxN = noise * max_arc_dist
    random_noise = randomGen.uniform(-maxN, maxN)
    self.noise_distance = max(0, self.distance + random_noise)
    summation = self.noise_succesful + self.no_noise_succesful
    rand_number = randomGen.random()
    if rand_number < self.no_noise_succesful / summation:
      self.distance = self.normal_distance
      self.distanceType = 0  # No noise is used in the objective solution
    else:
      self.distance = self.noise_distance
      self.distanceType = 1  # Noise is used in the objective solution
    return self.distance

  def calculateMaxArc(self):
    max_arc_length = 0
    for route in self.routes:
      for i in range(1, len(route.locations)):
        first_node_id = route.locations[i - 1].id
        second_node_id = route.locations[i].id
        arc_length = self.problem.distMatrix[first_node_id][second_node_id]
        if arc_length > max_arc_length:
          max_arc_length = arc_length
    return max_arc_length

  def executeRandomRemoval(self, nRemove, randomGen):
    """
    Method that executes a random removal of requests
    
    This is destroy method number 1 in the ALN
    Parameters
    ----------
    nRemove : int
        number of requests that is removed.
             
    Parameters
    ----------
    randomGen : Random
        Used to generate random number
    """
    for i in range(nRemove):
        # terminate if no more requests are served
        if len(self.served) == 0:
            break
        # pick a random request and remove it from the solutoin
        req = randomGen.choice(self.served)
        self.removeLocation(req)
    self.distance = self.computeDistance()
  
  def removeLocation(self, location):
    """
    Method that removes a request from the solution
    """
    # iterate over routes to find in which route the request is served
    for route in self.routes:
      if location in route.locations:
        # remove the request from the route and break from loop
        route.removeLocation(location)
        break
    # update lists with served and unserved requests
    # print(self.served)
    # print(location)
    self.served.remove(location)
    self.notServed.append(location)
    # revise update distance
    # self.computeDistance()
  
  def addLocation(self, location, insertRoute, node_index):
    '''
    Method that add a request to the solution
    '''
    if insertRoute == None:
      locList = [self.problem.depot, location, self.problem.depot]
      newRoute = Route(locList, self.problem)
      self.routes.append(newRoute)
      self.distance += newRoute.distance
    else:
      for route in self.routes:
        if route == insertRoute:
          res = route.addLocation(location, node_index)
          if res == -1:
            locList = [self.problem.depot, location, self.problem.depot]
            newRoute = Route(locList, self.problem)
            self.routes.append(newRoute)
            self.distance += newRoute.distance
          else:
            self.distance += res
    # update lists with served and unserved requests
    self.served.append(location)
    self.notServed.remove(location)
    # update distance
    # self.computeDistance()
  
  def copy(self):
    """
    Method that creates a copy of the solution and returns it
    """
    # need a deep copy of routes because routes are modifiable
    routesCopy = list()
    for route in self.routes:
      routesCopy.append(route.copy())
    copy = Solution(self.problem, routesCopy, self.served.copy(), self.notServed.copy())
    copy.computeDistance()
    return copy
  
  def executeRandomInsertion(self, randomGen):

    """
    Method that randomly inserts the unserved requests in the solution
    
    This is repair method number 1 in the ALNS
    
    Parameters
    ----------
    randomGen : Random
        Used to generate random numbers
    """
    # iterate over the list with unserved requests
    while len(self.notServed) > 0:
      # pick a random request
      location = randomGen.choice(self.notServed)
      # keep track of routes in which req could be inserted
      potentialRoutes = self.routes.copy()
      inserted = False
      while len(potentialRoutes) > 0:
        # pick a random route
        randomRoute = randomGen.choice(potentialRoutes)
        afterInsertion, cost = randomRoute.greedyInsert(location)
        if afterInsertion == None:
          # insertion not feasible, remove route from potential routes
          potentialRoutes.remove(randomRoute)
        else:
          # insertion feasible, update routes and break from while loop
          inserted = True
          # print("Possible")
          self.routes.remove(randomRoute)
          self.routes.append(afterInsertion)
          self.distance += cost
          break
      # if we were not able to insert, create a new route
      if not inserted:
        # create a new route with the request
        locList = [self.problem.depot, location, self.problem.depot]
        newRoute = Route(locList, self.problem)
        self.routes.append(newRoute)
        self.distance += newRoute.distance
      # update the lists with served and notServed requests
      self.served.append(location)
      self.notServed.remove(location)
    # self.computeDistance()

  def print(self):
    """
    Method that prints the solution
    """
    nRoutes = len(self.routes)
    nNotServed = len(self.notServed)
    print('total distcance ' + str(self.distance) + " Solution with " + str(nRoutes) + " routes and " + str(
      nNotServed) + " unserved requests: ")
    for route in self.routes:
      route.print()
    print("\n\n")