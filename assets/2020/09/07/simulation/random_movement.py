import enum
import math

import numpy as np
import matplotlib.pyplot as plt


# Utility classes for typing the parameters
class BoundModeT(enum.Enum):
    CLIP = enum.auto()
    REROLL = enum.auto()

# Whether or not to even simulate the population
SIM_POP: bool = True
# How many people to simulate
POP_SIZE: int = 10000000
# How many times to move them to get to a steady state
NUM_STEPS: int = 30
# What standard deviation the people should move with
MOVE_SIGMA: float = 0.1
# How to handle people moving out of bounds
BOUND_MODE: BoundModeT = BoundModeT.REROLL
# How many bins to show when displaying
NUM_BINS: int = 100


# Derived parameters
BIN_DELTA: float = 1.0 / NUM_BINS

# Utility functions
def erfInt(x: float):
    # Antiderivative of math.erf
    return x * math.erf(x) + math.exp(-x**2) / math.sqrt(math.pi)


# Compute the expected values as eigenvectors of a markov matrix
# Note the indexing convention - rows are destinations and columns are sources
# This is done for easier eigenvector computation later
# Also note that we reuse computations for different modes

markovMat: np.ndarray = np.empty( (NUM_BINS+2, NUM_BINS+2) )

if BOUND_MODE == BoundModeT.CLIP or BOUND_MODE == BoundModeT.REROLL:

    # Probability of going into the boundaries and clipping
    markovMat[0][0] = markovMat[-1][-1] = 0.5
    markovMat[-1][0] = markovMat[0][-1] = 1/2 * (1 + math.erf(-1 / (math.sqrt(2) * MOVE_SIGMA)))
    for b in range(1, NUM_BINS+1):
        # Compute the coefficients needed to calculate the integral
        intScale = MOVE_SIGMA / (math.sqrt(2.0) * BIN_DELTA)
        bScale = -BIN_DELTA / (math.sqrt(2) * MOVE_SIGMA)
        # Use symmetry
        markovMat[0][b] = 1/2 - intScale * (erfInt(b*bScale) - erfInt((b-1)*bScale))
        markovMat[-1][NUM_BINS+1-b] = markovMat[0][b]

    # Probability of escaping the boundaries with clipping
    for b in range(1, NUM_BINS+1):
        # Compute coefficients
        bScale = BIN_DELTA / (math.sqrt(2.0) * MOVE_SIGMA)
        # Again, leverage symmetry
        markovMat[b][0] = 1/2 * (math.erf(b*bScale) - math.erf((b-1)*bScale))
        markovMat[NUM_BINS+1-b][-1] = markovMat[b][0]

    # Populate everything else
    for B in range(1, NUM_BINS+1):
        for b in range(1, NUM_BINS+1):
            # The coefficients out front
            intScale = MOVE_SIGMA / (math.sqrt(2.0) * BIN_DELTA)
            bBScale = BIN_DELTA / (math.sqrt(2.0) * MOVE_SIGMA)
            # The four terms in the integral
            t1P = erfInt( bBScale * (B - (b-1)) )
            t1N = erfInt( bBScale * ((B-1) - (b-1)) )
            t2P = -erfInt( bBScale * (B - b) )
            t2N = -erfInt( bBScale * ((B-1) - b))
            # The final value
            markovMat[b][B] = intScale * ( (t1P-t1N) + (t2P-t2N) )

    # If we aren't going to clip, removed those entries form the matrix
    # Renormalize everything else to have a probability of one
    if BOUND_MODE == BoundModeT.REROLL:
        # Remove clip states
        markovMat = np.delete(markovMat, [0,-1], axis=0)
        markovMat = np.delete(markovMat, [0,-1], axis=1)
        # Renormalize
        markovMat /= np.sum(markovMat, axis=0)


# Solve for the eigenvalue 1
# We already know it exists, so don't try to compute it
markovMatSize = markovMat.shape[0]
solMat = (markovMat - np.identity(markovMatSize))
solVec = np.zeros((markovMatSize,))
# When solving for the eigenvector, choose the one with a given population size
# - sum of entries is given
solMat[-1] = np.ones((markovMatSize,))
solVec[-1] = POP_SIZE
# Solve
sol = np.linalg.solve(solMat, solVec)

# Generate the expected distribution
expectedX: np.ndarray = np.linspace(0.0, 1.0, NUM_BINS)
expectedY: np.ndarray = None
expectedNumClipped: float = None
if BOUND_MODE == BoundModeT.CLIP:
    expectedY = sol[1:-1]
    expectedNumClipped = sol[0] + sol[-1]
elif BOUND_MODE == BoundModeT.REROLL:
    expectedY = sol


# Only simulate if we were instructed to
if SIM_POP:
    # Generate our population on the unit interval
    population: np.ndarray = np.random.uniform( size=(POP_SIZE,) )
    # Move them around to get to a steady state
    for i in range(NUM_STEPS):
        # Move around, minding how we bound
        # Emulate a do-while loop for this
        dx = np.random.normal(scale=MOVE_SIGMA, size=(POP_SIZE,))
        while True:
            population += dx
            # If we're clipping, clip and be done with it
            if BOUND_MODE == BoundModeT.CLIP:
                population = np.clip(population, 0.0, 1.0)
                break
            # If we should reroll, reroll those we need
            elif BOUND_MODE == BoundModeT.REROLL:
                outIdx = (population <= 0.0) | (population >= 1.0)
                numOut = np.sum(outIdx)
                if numOut != 0:
                    population[outIdx] -= dx[outIdx]
                    dx[~outIdx] = 0.0
                    dx[outIdx] = np.random.normal(scale=MOVE_SIGMA, size=(numOut,))
                else:
                    break



# Print the proportion clipped if we're clipping
if BOUND_MODE == BoundModeT.CLIP:
    # Find who got clipped and how many did
    clippedIdx = (population == 0.0) | (population == 1.0)
    numClipped = np.sum(clippedIdx)
    # Print the results
    print(f"Clipped {numClipped} vs {expectedNumClipped} " + \
        f"({100.0 * abs(numClipped - expectedNumClipped) / (expectedNumClipped)}% Error)")
    # Remove the clipped people from the histogram
    population = np.delete(population, clippedIdx)

# Create the plot
fig, ax = plt.subplots()
# Plot the histogram (if we need to) and the expected distribution
if SIM_POP:
    ax.hist(population, bins=NUM_BINS)
ax.plot(expectedX, expectedY)
# Format the results
ax.set_frame_on(True)
ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, None)
# Show
plt.show()
