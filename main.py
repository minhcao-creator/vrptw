from vrptw import VRPTW
from alns import ALNS

test = "Instances/post.json"
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
alns.execute()