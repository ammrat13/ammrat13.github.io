import itertools

# Configuration variable
# How many numbers there are
N = 6
# The day list to check
# Must have N-1 days, each with number 0, 1, ..., N-1
DAY_LIST = [
    [1,0,3,2,4,5],
    [2,4,0,5,1,3],
    [3,5,4,0,2,1],
    [4,3,5,1,0,2],
    [5,2,1,4,3,0],
]


# Get the path down starting at an index
def path_down(start, days):
    ret = [start]
    cur = start
    for day in days:
        ret.append(day[cur])
        cur = day[cur]
    return ret

# Check if a list is a permutation
def is_perm(xs):
    return sorted(xs) == list(range(len(xs)))


# Check all the possible reorderings of the days
for day_perm in itertools.permutations(DAY_LIST):
    for start in range(N):
        if is_perm(path_down(start,day_perm)):
            print("Found")
