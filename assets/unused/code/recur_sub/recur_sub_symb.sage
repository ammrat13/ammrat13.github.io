# Configuration Variables:

# The number of terms to compute, including the constant
N_TERMS = 30

# The terms of the recursive formula
# Each tuple has the format (constant, x_power, y_power)
# Make sure to declare the variables used first
# Declare used variables
A,B = var('A B')
RECUR_FORMULA = [
    (1,3,0),
    (A,1,2),
    (B,0,3),
]



# Set some preliminary variables based off RECUR_FORMULA
min_indep_xpow = min([t[1] for t in filter(lambda t: t[2] == 0, RECUR_FORMULA)])
max_ypow = max([t[2] for t in RECUR_FORMULA])

# Create our array for dynamic programming, making sure we don't shallow copy
# dp_arr[iy][ix] is the coefficent of x**(ix + iy*min_indep_xpow) in y**iy
dp_arr = [[0]*N_TERMS for _ in range(max_ypow+1)]
# Note that y**0 is known to be 1
dp_arr[0][0] = 1



# Do the computation
for x_power_off in range(N_TERMS):


    # First phase of the computation deals with y**1
    # The result is simply the sum of the contributions from each of the terms
    y1_sum = 0
    for term in RECUR_FORMULA:

        # Extract the components
        c, xp, yp = term

        # Compute the index to access and check its validity
        # Mainly for ix, where we solve
        #  1*min_xpow + x_power_off == (ix + iy*min_xpow) + xp
        iy = yp
        ix = x_power_off - (iy-1)*min_indep_xpow - xp
        if iy != 0 and ix >= x_power_off:
            raise IndexError(f"Trying to read from invalid DP: {iy} {ix}")

        # Add the contribution, checking for negative
        # Contribution is zero in that case
        if ix >= 0:
            y1_sum += c * dp_arr[iy][ix]

    # Set the result
    dp_arr[1][x_power_off] = y1_sum


    # Compute all the higher powers of y
    for y_power in range(2, max_ypow+1):

        # Just sum over all the terms in y**(y_power - 1) * y
        cum_sum = 0
        for xo in range(x_power_off+1):
            cum_sum += dp_arr[y_power-1][xo] * dp_arr[1][x_power_off - xo]

        # Assign
        dp_arr[y_power][x_power_off] = cum_sum



# Print out the result
# Correct for the offset of min_indep_xpow on the first row
# Also expand the expressions
print([0]*min_indep_xpow + [expand(x) for x in dp_arr[1]])
