# Import for typing
from typing import NewType
from typing import List, Optional, Callable
# Utilities for iteration and functions
from itertools import product, chain
from functools import partial
# Math functions
from math import gcd
# For command line parameters
from sys import argv



# Typedefs for graph size, vertices, and colors
GraphSize = int
Vertex = NewType('Vertex', int)
Color = NewType('Color', int)



class EvenCompleteEdgeColoring:

    def __init__(self, n: GraphSize):
        """
        Initialize this edge coloring on a complete graph with an even number of
        vertices.
        """

        # Check that n is even
        if n % 2 != 0:
            raise ValueError(f"Number of vertices must be even: {n}")

        # Set variables
        self.n = n


    def check(self) -> bool:
        """
        Verify that this coloring is a proper coloring. Go through all the
        vertices and check that they satisfy the conditions.
        """

        # Generate our vertex and edge set
        V = list(map(Vertex, range(self.n)))
        E = list(product(V, repeat=2))
        # Set of allowed colors
        C = list(map(Color, range(self.n-1)))

        # First, check the set of edges
        for u,v in E:
            # Break into cases on if the vertices are equal
            if u == v:
                # Must have that the color is None
                if self.color_of(u,v) != None:
                    return False
            if u != v:
                # Must have that the color is not None
                # Must have the same color in both directions
                # Must be between 0 and n-2 (check in last for loop)
                if self.color_of(u,v) == None \
                or self.color_of(u,v) != self.color_of(v,u):
                    print(f"Here {u} {v}")
                    return False

        # Check that each of the vertices are connected to each color exactly
        #  once, excluding themselves for None
        # Also checks that all the colors are between 0 and n-2 inclusive
        for u in V:
            colors_have = set(map(partial(self.color_of, u), V))
            colors_want = set(chain(C, [None]))
            if colors_have != colors_want:
                return False

        # If we haven't returned False yet, we're good
        return True


    def color_of(self, u: Vertex, v: Vertex) -> Color:
        """
        Returns the color between any two vertices.
        """

        # Check that the vertices are valid
        if u < 0 or u >= self.n \
        or v < 0 or v >= self.n:
            raise ValueError(f"Invalid vertex numbers: {u} {v}")

        # Check for equality
        if u == v:
            return None


        # Base case if n is an odd multiple of two
        if (self.n // 2) % 2 != 0:

            # Ensure u comes before v in the direction of least difference
            # Does not ensure that u < v
            if (v-u) % self.n > self.n//2:
                u,v = v,u

            # Get the difference
            diff = (v-u) % self.n

            # Check for midlines
            if diff == self.n // 2:
                return Color(min(u,v))

            # Check for perpendiculars
            if diff % 2 == 0:
                midline_num = ((u+v)//2) % (self.n//2)
                return Color(midline_num)

            # Otherwise, its part of an even cycle
            cycle_num = u % gcd(self.n, diff)
            return Color((self.n//2) + (diff-1) + (u-cycle_num)%2)


        else:

            # Ensure that u and v are sorted in increasing order
            # Does not ensure that v-u is the minimal distance between them
            if u > v:
                u,v = v,u

            # Get offsets in respective blocks
            u_mod = u % (self.n//2)
            v_mod = v % (self.n//2)

            # If they are in different blocks, color accordingly
            # Note that != functions as XOR
            if (u < self.n//2) != (v < self.n//2):
                # The offset between the offsets
                diff = (v_mod - u_mod) % (self.n//2)
                # Return the color
                # Each half uses 0 to self.n//2 - 2 inclusive
                return Color(diff + self.n//2 - 1)

            # If they are in the same half, recurse
            else:
                return EvenCompleteEdgeColoring(self.n // 2) \
                    .color_of(u_mod, v_mod)




if __name__ == '__main__':
    res: bool = all(map(
        lambda n: EvenCompleteEdgeColoring(n).check(),
        range(2, int(argv[1]), 2)
    ))
    print(res)
