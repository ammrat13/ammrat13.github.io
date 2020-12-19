# Command line argument for size
from sys import argv
# Import our Python code
from even_complete_edge_coloring import EvenCompleteEdgeColoring

# Size of the graph
n = int(argv[1])
# The graph itself
G = graphs.CompleteGraph(n)
# The edge colors
C = EvenCompleteEdgeColoring(n)

# Set the labels
for u,v,_ in G.edges():
    G.set_edge_label(u, v, C.color_of(u,v))

P = G.graphplot(color_by_label=True)
P.plot().save("out.png")
