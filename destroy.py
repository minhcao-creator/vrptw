import numpy as np

class Destroy:
  
  def __init__(self, problem, solution):
    self.problem = problem
    self.solution = solution
  
  def findWorstCostRequest(self):
    cost = []
    # Making list with request ID's and their corresponding cost
    for route in self.solution.routes:
      for i in range(2, len(route.locations)):
        first_node_id = route.locations[i - 2].id
        middle_note_id = route.locations[i - 1].id
        last_node_id = route.locations[i].id
        dist = self.problem.distMatrix[first_node_id][middle_note_id]+self.problem.distMatrix[middle_note_id][last_node_id]
        cost.append(dist)
    # Sort cost
    cost = sorted(cost)
    chosen_location = None
    # Get request object that corresponds to worst cost 
    worst_cost_request_id = cost[-1]
    for loc in self.solution.served:
      if loc.id == worst_cost_request_id:
        chosen_location = loc
        break
    return chosen_location

  def findRandomRoute(self, randomGen):
    # First make a copy of the routes in the solution
    set_of_routes = self.solution.routes.copy()
    # Find select a random route that contains at least one request
    while True:
      if not set_of_routes:
        return None
      route = randomGen.choice(set_of_routes)
      # If no request can be removed from this route
      if len(route.locations) < 4:
        set_of_routes.remove(route)
      else:
        return route
    
  def findWorstCostRequestRandomRoute(self, randomGen):
    route = self.findRandomRoute(randomGen)
    cost = []
    # Making list with request ID's and their corresponding cost
    for i in range(2, len(route.locations)):
      first_node_id = route.locations[i - 2].id
      middle_note_id = route.locations[i - 1].id
      last_node_id = route.locations[i].id
      dist = self.problem.distMatrix[first_node_id][middle_note_id]+self.problem.distMatrix[middle_note_id][last_node_id]
      cost.append(dist)
    # Sort cost
    cost = sorted(cost)
    chosen_location = None
    # Get request object that corresponds to worst cost 
    worst_cost_request_id = cost[-1]
    for loc in self.solution.served:
      if loc.id == worst_cost_request_id:
        chosen_location = loc
        break
    return chosen_location

  def findStartingLocationShaw(self, randomGen):
    # Choose random route
    potentialRoutes = self.solution.routes
    location = None
    # Revise.
    while potentialRoutes:
      route = randomGen.choice(potentialRoutes)
      # Might exist the situation of [depot, depot]
      if len(route.locations) > 2:
        # From this route, choose a random location which is not the depot
        for location in route.locations:
          print(location.id)
        location = randomGen.choice([location for location in route.locations if location.id != 0])
        break
      else:
        potentialRoutes.remove(route)
    return location
  
  def findNextShawRequest(self):
    # Initialize key variables and location that is currently selected
    locations, distances, readies, demands = [], [], [], []
    loc_i = self.last_shaw_location
    # Define values of key variables for location i
    location_i, ready_i, demand_i = loc_i.id, loc_i.ready, loc_i.demand
    # Find values of key variables for all other locations
    for route in self.solution.routes:
      for loc_j in route.locations:
        # Only consider locations which are not depots
        if loc_j.id != 0:
          locations.append(loc_j)
          location_j, ready_j, demand_j = loc_j.id, loc_j.ready, loc_j.demand
          # Find difference of the two nodes in terms of the key variables
          distance_diff = self.problem.distMatrix[location_i][location_j]
          ready_diff = abs(ready_i-ready_j)
          demand_diff = abs(demand_i-demand_j)
          # Add differences to the lists of key variables
          distances.append(distance_diff)
          readies.append(ready_diff)
          demands.append(demand_diff)
    # Normalize values
    if sum(readies):
      normalized_readies = list(map(lambda x: x / sum(readies), readies))
    else:
      normalized_readies = readies
    if sum(distances):
      normalized_distances = list(map(lambda x: x / sum(distances), distances))
    else:
      normalized_distances = distances
    if sum(demands):
      normalized_demands = list(map(lambda x: x / sum(demands), demands))
    else:
      normalized_demands = demands
    # normalized_distances = list(map(lambda x:x/sum(distances), distances))
    # normalized_start_tws = list(map(lambda x:x/sum(start_tws), start_tws))
    # normalized_demands = list(map(lambda x:x/sum(demands), demands)
    # Calculate relatednesses to each location based on the normalized values
    relatednesses = []
    for index, location in enumerate(locations):
      relatednesses.append((location,
                            normalized_distances[index] +
                            normalized_readies[index] +
                            normalized_demands[index]))
    # Sort locations based on relatednesses and choose most related one
    relatednesses = sorted(relatednesses, key = lambda r: r[1], reverse = False)
    self.last_shaw_location = relatednesses[0][0]
    # Determine request that is related to the most related location
    chosen_location = None
    for loc in self.solution.served:
      if loc.id == self.last_shaw_location.id:
        chosen_location
    return chosen_location

  def findNextProximityBasedRequest(self):
    # Initialize location that is currently selected
    loc_i = self.last_proximity_location
    closest = np.inf
    # Find closest location in terms of distance
    for route in self.solution.routes:
      for loc_j in route.locations:
        # Only consider locations which are not depots
        if loc_j.id != 0:
          distance_diff = self.problem.distMatrix[loc_i.id][loc_j.id]
          if distance_diff < closest:
            chosen_location = loc_j
            closest = distance_diff
    self.last_proximity_location = chosen_location
    # Determine request that is related to the closest location
    chosen_loc = None
    for loc in self.solution.served:
      if loc.id == self.last_proximity_location.id:
        chosen_loc
    return chosen_loc

  def findNextDemandBasedRequest(self):
    # Initialize location that is currently selected
    loc_i = self.last_demand_based_location
    smallest_diff = np.inf
    # Find most related location in terms of demand
    for route in self.solution.routes:
      for loc_j in route.locations:
        # Only consider locations which are not depots
        if loc_j.id != 0:
          demand_diff = abs(loc_i.demand - loc_j.demand)
          if demand_diff < smallest_diff:
            chosen_location = loc_j
            smallest_diff = demand_diff
    self.last_demand_based_location = chosen_location
    chosen_loc = None
    # Determine request that is related to the closest location
    for loc in self.solution.served:
      if loc.id == self.last_demand_based_location.id:
        chosen_loc = loc
        break
    return chosen_loc

  def executeRandomRemoval(self, nRemove, randomGen):
    # print('nRemove = ' + str(nRemove))
    for _ in range(nRemove):
      # terminate if no more requests are served
      if len(self.solution.served) == 0:
        break
      # pick a random request and remove it from the solutoin
      # print(self.solution.served)
      loc = randomGen.choice(self.solution.served)
      if loc != None:
        self.solution.removeLocation(loc)
  
  def executeWorstCostRemoval(self, nRemove):
    for _ in range(nRemove):
      if len(self.solution.served) == 0:
        break
      chosen_loc = self.findWorstCostRequest()
      # print("Chosen request:")
      # print(chosen_req)
      # print("\n")
      if chosen_loc != None:
        self.solution.removeLocation(chosen_loc)
      
  def executeRandomRouteRemoval(self, nRemove, randomGen):
    for _ in range(nRemove):
      if len(self.solution.served) == 0:
        break
      chosen_loc = self.findWorstCostRequestRandomRoute(randomGen)
      # print("Chosen request:")
      # print(chosen_req)
      # print("\n")
      if chosen_loc != None:
        self.solution.removeLocation(chosen_loc)
  
  def executeShawRequestRemoval(self, nRemove, randomGen):
    if len(self.solution.served) == 0:
      return
    # Initialize starting location based on randomGen
    location = self.findStartingLocationShaw(randomGen)
    self.last_shaw_location = location
    # Select corresponding request
    location_id = location.id
    for loc in self.solution.served:
      if loc.id == location_id:
        self.solution.removeLocation(loc)
        break
    # Remove next requests based on relatednesses between locations
    for _ in range(nRemove-1):
      if len(self.solution.served) == 0:
        break
      chosen_loc = self.findNextShawRequest()
      # print("Chosen request:")
      # print(chosen_req)
      # print("\n")
      if chosen_loc != None:
        self.solution.removeLocation(chosen_loc)
      
  def executeProximityBasedRemoval(self, nRemove, randomGen):
    if len(self.solution.served) == 0:
      return
    # Initialize starting location
    location = self.findStartingLocationShaw(randomGen)
    self.last_proximity_location = location
    # Select corresponding request
    location_id = location.id
    for loc in self.solution.served:
      if loc.id == location_id:
        self.solution.removeLocation(loc)
        break
    # Remove next requests based on relatedness in terms of distance between locations
    for _ in range(nRemove-1):
      if len(self.solution.served) == 0:
        break
      chosen_loc = self.findNextProximityBasedRequest()
      # print("Chosen request:")
      # print(chosen_req)
      # print("\n")
      if chosen_loc != None:
          self.solution.removeLocation(chosen_loc)
        
  def executeDemandBasedRemoval(self, nRemove, randomGen):
    if len(self.solution.served) == 0:
      return
    # Initialize starting location
    location = self.findStartingLocationShaw(randomGen)
    self.last_demand_based_location = location
    # Select corresponding request
    location_id = location.id
    for loc in self.solution.served:
      if loc.id == location_id:
        self.solution.removeLocation(loc)
        break
    # Remove next requests based on relatedness in terms of start time windows between locations
    for _ in range(nRemove-1):
      if len(self.solution.served) == 0:
        break
      chosen_loc = self.findNextDemandBasedRequest()
      # print("Chosen request:")
      # print(chosen_req)
      # print("\n")
      if chosen_loc != None:
        self.solution.removeLocation(chosen_loc)
