import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon
from steinernet.steiner import SteinerNet
from steinernet.random_walk_subgraph import random_walk_tree as random_walk_subgraph

# Base graph

base_graph = nx.complete_graph(10)
for u, v in base_graph.edges():
    base_graph[u][v]['weight'] = random.randint(1, 10)

# Terminals
terminals = random.sample(list(base_graph.nodes()), 5)

# Generate Steiner base graph using random walk
G = random_walk_subgraph(base_graph, terminals, seed=42)

# Filter terminals to only those present in G
terminals = [t for t in terminals if t in G.nodes]
print("G nodes:", list(G.nodes))
print("Terminals used for benchmarking:", terminals)

# Visualize
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightgray')
nx.draw_networkx_nodes(G, pos, nodelist=terminals, node_color='orange')
plt.title("Base Steiner Graph (Random Walk)")
plt.show()



methods = ['SP', 'KB', 'RSP', 'SPM', 'ASP', 'EXA','MEXA','EXA+']# 'RW' is a random walk subgraph, not a tree method
print
results = []
sn = SteinerNet(G)

for method in methods:
    times = []
    scores = []
    for _ in range(1):
        print(f"Method: {method}:")
        start = time.time()
        tree = sn.steinertree(terminals, method=method, repeats=5, optimize=True)
        end = time.time()
        times.append(end - start)
        print(f"Time taken: {end - start:.4f} seconds")
        print(f"Tree size: {tree.size(weight='weight')}")
        print(f"Tree edges: {list(tree.edges(data=True))}")
        print(f"Tree nodes: {list(tree.nodes())}")
        scores.append(tree.size(weight='weight'))   
    for score, t in zip(scores, times):
        results.append({"method": method, "score": score, "time": t})

bench_df = pd.DataFrame(results)
