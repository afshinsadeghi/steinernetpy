import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from steinernet.steiner import SteinerNet
from steinernet.random_walk_subgraph import random_walk_tree

# Base graph
base_graph = nx.complete_graph(10)
for u, v in base_graph.edges():
    base_graph[u][v]['weight'] = random.randint(1, 10)

# Terminals
terminals = random.sample(list(base_graph.nodes()), 5)

# Generate Steiner base graph using random walk
G = random_walk_tree(base_graph, terminals, seed=42)

# Filter terminals to only those present in G
terminals = [t for t in terminals if t in G.nodes]
print("G nodes:", list(G.nodes))
print("Terminals used for benchmarking:", terminals)

# Run KB method
print("\nRunning KB method...")
try:
    sn = SteinerNet(G)
    tree = sn.steinertree(terminals, method='KB', repeats=5, optimize=True)
    print("KB method succeeded!")
    print(f"Tree size: {tree.size(weight='weight')}")
    print(f"Tree edges: {list(tree.edges(data=True))}")
    print(f"Tree nodes: {list(tree.nodes())}")
except Exception as e:
    print(f"KB method failed with error: {e}")
