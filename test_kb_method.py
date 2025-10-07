import networkx as nx
import random
from steinernet.steiner import SteinerNet
from steinernet.random_walk_subgraph import random_walk_tree

# Create a base graph
base_graph = nx.complete_graph(10)
for u, v in base_graph.edges():
    base_graph[u][v]['weight'] = random.randint(1, 10)

# Select terminals
terminals = random.sample(list(base_graph.nodes()), 5)

# Generate Steiner base graph using random walk
G = random_walk_tree(base_graph, terminals, seed=42)

# Filter terminals to only those present in G
terminals = [t for t in terminals if t in G.nodes]
print("G nodes:", list(G.nodes))
print("Terminals used for benchmarking:", terminals)

# Create SteinerNet instance
sn = SteinerNet(G)

# Try to run the KB method
try:
    print("Running KB method...")
    tree = sn.steinertree(terminals, method='KB', repeats=5, optimize=True)
    print("KB method succeeded!")
    print(f"Tree size: {tree.size(weight='weight')}")
    print(f"Tree edges: {list(tree.edges(data=True))}")
    print(f"Tree nodes: {list(tree.nodes())}")
except Exception as e:
    print(f"KB method failed with error: {e}")

# Try to run the SP method for comparison
try:
    print("\nRunning SP method...")
    tree = sn.steinertree(terminals, method='SP', repeats=5, optimize=True)
    print("SP method succeeded!")
    print(f"Tree size: {tree.size(weight='weight')}")
    print(f"Tree edges: {list(tree.edges(data=True))}")
    print(f"Tree nodes: {list(tree.nodes())}")
except Exception as e:
    print(f"SP method failed with error: {e}")
