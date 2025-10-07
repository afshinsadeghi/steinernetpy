# pysteinernet/random_walk_tree.py

"""
Random Walk-Based Steiner Tree Generator

This module generates approximate Steiner trees using a random walk strategy.

@reference
Afshin Sadeghi and Holger Froehlich, "Steiner tree methods for optimal sub-network identification: an empirical study",
BMC Bioinformatics 2013 14:144, doi:10.1186/1471-2105-14-144
"""

import networkx as nx
import random

def random_walk_subgraph(G: nx.Graph, terminals: list[int], seed: int = None) -> nx.Graph:
    """
    Generate a sub graph using a random walk strategy given a graph and set of terminal nodes.

    This method generates a subgraphs by iteratively performing random walks
    from already connected terminals until all terminals are spanned.

    Parameters:
    G (nx.Graph): Input undirected graph with optional weights.
    terminals (list[int]): List of terminal node indices to connect.
    seed (int, optional): Random seed for reproducibility.

    Returns:
    nx.Graph: A subgraph using random walks.

    Example:
    >>> import networkx as nx
    >>> from steinernet.random_walk_subgraph import random_walk_subgraph
    >>> G = nx.cycle_graph(6)
    >>> terminals = [0, 2, 4]
    >>> T = random_walk_subgraph(G, terminals, seed=42)
    >>> nx.draw(T, with_labels=True)

    Reference:
    - https://github.com/afshinsadeghi/SteinerNet/blob/master/R/random_walk.R
    - Afshin Sadeghi and Holger Froehlich, BMC Bioinformatics 2013 14:144
    """
    if seed is not None:
        random.seed(seed)

    terminals = list(terminals)
    connected = set([random.choice(terminals)])
    tree = nx.Graph()

    while not all(t in connected for t in terminals):
        current = random.choice(list(connected))
        path = [current]

        while True:
            neighbors = list(G.neighbors(current))
            if not neighbors:
                break
            next_node = random.choice(neighbors)
            path.append(next_node)
            current = next_node

            if current in terminals and current not in connected:
                connected.add(current)
                break

        nx.add_path(tree, path)
        for u, v in zip(path[:-1], path[1:]):
            if G.has_edge(u, v):
                tree.add_edge(u, v, weight=G[u][v].get('weight', 1.0))

    return tree

# Add an alias for backward compatibility
random_walk_tree = random_walk_subgraph
