import typing
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Set the matplotlib backend, else it complains
matplotlib.use('Qt5Agg')


# The initial size of the population
POP_SIZE: int = 1000000
# The initial proportion of infected people
PROP_INITIAL_INFECTED: float = .01
# The probability of one person getting infected by one other person during one
# second of the simulation
P_INFECT: float = .75
# How long each timestep is in seconds
DT: float = 2.5e-9
# How many seconds to simulate for
NUM_SECONDS: float = 1e-5

# The probability of one person getting infected by one other person during only
# one timestep
P_INFECT_DT: float = 1 - (1-P_INFECT)**DT
# How many steps to simulate for
NUM_STEPS: int = round(NUM_SECONDS / DT)


# Function to compute the expected number of infected people at a given time
def get_infected(t: float) -> float:
    # Compute the proportionality constant in the diff eq
    r = -POP_SIZE * math.log(1 - P_INFECT)
    # Compute the initial condition
    x0 = PROP_INITIAL_INFECTED
    # Steal the solution from Wolfram Mathworld
    return POP_SIZE / (1 + (1/x0 - 1) * math.exp(-r*t))

# Function to compute the expected number of newly infected people given the
# current number of infected people. Comes in variants for over the next second
# and over the next timestep.
def get_dinfected_dt(infected: int) -> float:
    return -math.log(1 - P_INFECT) * infected * (POP_SIZE - infected)
def get_dinfected(infected: int) -> float:
    return DT * get_dinfected_dt(infected)


# The time array on which we operate
time_values = np.linspace(0.0, NUM_SECONDS, num=NUM_STEPS)
# The initial number of infected people
infected: int = round(POP_SIZE * PROP_INITIAL_INFECTED)
# An array in which we store the final count of infected people and the number
# of newly infected people. Also store the expected infected and newly infected
result_infected: typing.List[int] = []
result_newly_infected: typing.List[int] = []
result_expected_infected: typing.List[int] = []
result_expected_newly_infected: typing.List[int] = []

# Simulate forward
for t in time_values:
    # Compute how many people are healthy
    healthy: int = POP_SIZE - infected
    # Compute what healthy people get infected
    # We don't care how many times they got infected, just if they did
    whogot_infected = np.random.binomial(infected, P_INFECT_DT, (healthy,)) >= 1
    # Compute how many people get infected
    newly_infected = np.sum(whogot_infected)

    # Update
    result_infected.append(infected)
    result_newly_infected.append(newly_infected)
    result_expected_infected.append(get_infected(t))
    result_expected_newly_infected.append(get_dinfected(infected))
    infected += newly_infected

# First figure for plot of total infected over time
plt.figure()
plt.plot(
    time_values, result_infected,
    time_values, result_expected_infected)
plt.xlabel("Time")
plt.ylabel("Total Infected")
# Second figure is plot of newly infected vs. current infected
# Also show the expected value
plt.figure()
plt.plot(
    result_infected, result_newly_infected, '.',
    result_infected, result_expected_newly_infected)
plt.xlabel("Total Infected")
plt.ylabel("Newly Infected")
# Show it all
plt.show()
