from vrptw import VRPTW
from alns import ALNS

import json
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)

@app.route('/vrp', methods=['POST'])
@cross_origin()
def create_employee():
  test = json.loads(request.data)
  print(test)
  if not test:
    return jsonify({ 'error': 'Invalid datadata.' }), 400
  problem = VRPTW.readInstance(test)

  # Static parameters
  nDestroyOps = 6
  nRepairOps = 3
  minSizeNBH = 1
  nIterations = 20000

  # Parameters to tune:
  maxPercentageNHB = 5
  tau = 0.03
  coolingRate = 0.9990
  decayParameter = 0.15
  noise = 0.015

  alns = ALNS(problem, nDestroyOps, nRepairOps, nIterations, minSizeNBH, maxPercentageNHB, tau, coolingRate, decayParameter, noise)
  response = []
  routes = alns.execute()
  for route in routes:
    locations = route.locations
    res = []
    for loc in locations:
      res.append(loc.id)
    response.append(res)

  print(response)

  return response

if __name__ == '__main__':
  app.run(port=5000)

# test = "Instances/post.json"
# problem = VRPTW.readInstance(test)

# # Static parameters
# nDestroyOps = 6
# nRepairOps = 3
# minSizeNBH = 1
# nIterations = 20000

# # Parameters to tune:
# maxPercentageNHB = 5
# tau = 0.03
# coolingRate = 0.9990
# decayParameter = 0.15
# noise = 0.015

# alns = ALNS(problem, nDestroyOps, nRepairOps, nIterations, minSizeNBH, maxPercentageNHB, tau, coolingRate, decayParameter, noise)
# alns.execute()