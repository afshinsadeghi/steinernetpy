# steinerpy/steiner.py

"""
Steiner Tree Algorithms Interface

This module implements various heuristic and exact methods for computing Steiner trees on graphs.

@references
1. Petter, L., Hammer. Path heuristic and Original path heuristic, Section 4.1.3 of the book "The Steiner tree Problem"
2. H. Takahashi and A. Matsuyama, "An approximate solution for the Steiner problem in graphs"
3. F. K. Hwang, D. S. Richards and P. Winter, "The Steiner Tree Problem", Kruskal-Based Heuristic, Section 4.1.4, ISBN: 978-0-444-89098-6
4. Afshin Sadeghi and Holger Froehlich, "Steiner tree methods for optimal sub-network identification: an empirical study", BMC Bioinformatics 2013 14:144
5. F. K. Hwang, D. S. Richards and P. Winter, "The Steiner Tree Problem", Optimal solution for Steiner trees on networks, ISBN: 978-0-444-89098-6

Methods:
    - steinertree: Dispatch algorithm selector
    - SP: Shortest path heuristic [Ref 1]
    - KB: Kruskal-based heuristic [Ref 3]
    - RSP: Randomized shortest paths [Ref 4]
    - SPM: Union of Multiple Shortest path-based trees [Ref 4]
    - ASP: All shortest paths union [Ref 4]
    - EXA: Brute-force exact Steiner tree [Ref 5]
    - MEXA: Union subgraph of Brute-force exact Steiner trees [Ref 5]
    - EXA+: Exact algorithm union with local neighborhood explore to hop numbers [New: extention to EXA]
    - RW: Random walk subgraph [Ref 4]
"""

import networkx as nx
import random
import itertools
from .random_walk_subgraph import random_walk_subgraph

class SteinerNet:
    def __init__(self, G):
        """
        Initialize the SteinerNet interface on a given graph.
        :param G: networkx.Graph
        """
        self.G = G.copy()

    def steinertree(self, terminals, method='SP', repeats=70, optimize=True):
        """
        Unified interface to run one of several Steiner tree methods.
        :param terminals: List of terminal nodes
        :param method: String code for algorithm ('SP', 'KB', etc.)
        :param repeats: Number of repeats (for stochastic methods)
        :param optimize: Whether to prune extra nodes (only applies to some methods)
        :return: networkx.Graph (Steiner tree or approximation)
        """
        method = method.upper()
        if method == 'SP':
            return self._shortest_path_heuristic(terminals)
        elif method == 'KB':
            return self._key_node_based(terminals, repeats)
        elif method == 'RSP':
            return self._randomized_sp(terminals, repeats)
        elif method == 'SPM':
            return self._shortest_path_st_union(terminals)
        elif method == 'ASP':
            return self._all_shortest_paths_union(terminals)
        elif method == 'EXA':
            return self._exact_algorithm(terminals)
        elif method == 'MEXA':
            return self._exact_algorithm(terminals,union=True)
        elif method == 'EXA+':
            return self._exact_algorithm_union_with_neighbour_explore(terminals)
        elif method == 'RW':
            return self._random_walk(terminals)
        else:
            raise ValueError(f"Unknown method: {method}")

    def _random_walk(self, terminals):
        """
        Generate subgraph by random walks from terminals [Ref 4]
        """
        return random_walk_subgraph(self.G, terminals)

    def _shortest_path_heuristic(self, terminals):
        """
        Connect all terminal pairs via shortest paths and union the paths. [Ref 1]
        """
        T = nx.Graph()
        for i, t1 in enumerate(terminals):
            for t2 in terminals[i+1:]:
                try:
                    path = nx.shortest_path(self.G, t1, t2, weight='weight')
                    nx.add_path(T, path)
                except nx.NetworkXNoPath:
                    continue
        H = self.G.subgraph(T.nodes())
        mst = nx.minimum_spanning_tree(H, weight='weight')
        return self._prune_tree(mst, terminals)
        

    def _key_node_based(self, terminals, repeats):
        """
        Kruskal-based heuristic with random extra nodes. [Ref 3]     
        Replicates R's steinertree3:
        - Randomizes the order of terminals (except the first) each repeat
        - Grows tree by merging with shortest-paths
        - Extracts MST on the induced graph
        - Prunes non-terminal leaves
        - Keeps the minimum-weight tree across repeats
        """
        best_tree = None
        best_cost = float('inf')
        n = len(terminals)

        for _ in range(repeats):
            order = [terminals[0]] + random.sample(terminals[1:], k=n-1)
            edge_set = set()

            for i in range(1, n):
                u = order[i]
                try:
                    path = nx.shortest_path(self.G, source=order[0], target=u, weight='weight')
                except nx.NetworkXNoPath:
                    continue
                for a, b in zip(path[:-1], path[1:]):
                    edge_set.add((a, b))

            if not edge_set:
                continue

            sub = nx.Graph()
            for u, v in edge_set:
                sub.add_edge(u, v, weight=self.G[u][v]['weight'])
            # MST & prune
            mst = nx.minimum_spanning_tree(sub, weight='weight')
            mst = self._prune_tree(mst, terminals)
            cost = mst.size(weight='weight')

            if cost < best_cost:
                best_cost = cost
                best_tree = mst

        return best_tree

    def _randomized_sp(self, terminals, repeats):
        """
        Randomized permutation of terminal paths + pruning. [Ref 4]
        """
        best_tree = None
        best_score = float('inf')

        for _ in range(repeats):
            T = nx.Graph()
            t_perm = random.sample(terminals, len(terminals))
            for i in range(len(t_perm)-1):
                try:
                    path = nx.shortest_path(self.G, t_perm[i], t_perm[i+1], weight='weight')
                    nx.add_path(T, path)
                except nx.NetworkXNoPath:
                    continue
            T = self._prune_tree(T, terminals)
            score = T.size(weight='weight')
            if score < best_score:
                best_score = score
                best_tree = T

        return best_tree

    def _shortest_path_st_union(self, terminals):
        """
        Compute union of ST based tree which are gained over the union of shortest paths among terminals. [Ref 4]
        """
        edges_in_paths = set()
        for i, t1 in enumerate(terminals):
            for t2 in terminals[i+1:]:
                try:
                    path = nx.shortest_path(self.G, source=t1, target=t2, weight='weight')
                    for u, v in zip(path[:-1], path[1:]):
                        w = self.G[u][v]['weight']
                        edges_in_paths.add((u, v, w))
                except nx.NetworkXNoPath:
                    continue

        H = nx.Graph()
        for u, v, w in edges_in_paths:
            if H.has_edge(u, v):
                H[u][v]['weight'] = min(H[u][v]['weight'], w)
            else:
                H.add_edge(u, v, weight=w)

        return nx.minimum_spanning_tree(H, weight='weight')

    def _all_shortest_paths_union(self, terminals):
        """
        Union of all shortest paths among terminals (non-pruned). [Ref 4]
        """
        T = nx.Graph()
        for i, t1 in enumerate(terminals):
            for j, t2 in enumerate(terminals): #terminals[i+1:]:
                try:
                    path = nx.shortest_path(self.G, t1, t2, weight='weight')
                    print(f"Path between {t1} and {t2}: {path}")
                    nx.add_path(T, path)
                except nx.NetworkXNoPath:
                    continue
        return T

    def _exact_algorithm(self, terminals, union = False):
        """
        find Steiner trees, the Exact bruteforce method (mirrors R's SteinerExact):
        - Finds MSTs over all subsets of non-terminals
        - Collects *all* trees with minimal weight
        Returns: list of networkx.Graph
        """
        optimal_trees = []
        best_cost = float('inf')
        non_terminals = [n for n in self.G.nodes() if n not in terminals]

        for r in range(len(non_terminals) + 1):
            for subset in itertools.combinations(non_terminals, r):
                nodes_subset = set(terminals) | set(subset)
                subG = self.G.subgraph(nodes_subset)
                if nx.is_connected(subG):
                    T = nx.minimum_spanning_tree(subG, weight='weight')
                    cost = T.size(weight='weight')
                    if cost < best_cost:
                        best_cost = cost
                        optimal_trees = [T]
                    elif abs(cost - best_cost) < 1e-9:
                        optimal_trees.append(T)

        if union is False:
            return optimal_trees[0] 
        else:
            merged_edges = set()
            for tree in optimal_trees:
                merged_edges.update(tree.edges(data='weight'))

            merged_graph = nx.Graph()
            for u, v, w in merged_edges:
                if merged_graph.has_edge(u, v):
                    merged_graph[u][v]['weight'] = min(merged_graph[u][v]['weight'], w)
                else:
                    merged_graph.add_edge(u, v, weight=w)
    
            return merged_graph


    def _exact_algorithm_union_with_neighbour_explore(self, terminals, hops=2):
        """
        Find union of exact Steiner trees with local neighborhood expansion. [New]
        Adds nodes up to `hops` away from base tree and merges MSTs with same cost.
        """
        base_tree = self._exact_algorithm(terminals)
        if base_tree is None:
            return None
        best_cost = base_tree.size(weight='weight')

        nodes_in_tree = list(base_tree.nodes())
        candidate_nodes = set(nodes_in_tree)
        for node in nodes_in_tree:
            neighbors = nx.single_source_shortest_path_length(self.G, node, cutoff=hops)
            candidate_nodes.update(neighbors.keys())

        merged_edges = set(base_tree.edges(data='weight'))
        non_terminals = [n for n in candidate_nodes if n not in terminals]

        for r in range(len(non_terminals) + 1):
            for subset in itertools.combinations(non_terminals, r):
                nodes = list(terminals) + list(subset)
                subG = self.G.subgraph(nodes)
                if nx.is_connected(subG):
                    T = nx.minimum_spanning_tree(subG, weight='weight')
                    cost = T.size(weight='weight')
                    #if cost == best_cost:
                    if abs(cost - best_cost) < 1e-9: # to avoid floating point issues
                        merged_edges.update(T.edges(data='weight'))
                    if cost < best_cost:
                        best_cost = cost
                        merged_edges = set(T.edges(data='weight'))

        merged_graph = nx.Graph()
        for u, v, w in merged_edges:
            merged_graph.add_edge(u, v, weight=w)
        return merged_graph

    def _prune_tree(self, tree, terminals):
        """
        Remove non-terminal leaf nodes iteratively.
        """
        T = tree.copy()
        removable = [n for n in T.nodes() if n not in terminals]
        removed = True
        while removed:
            removed = False
            for n in removable[:]:
                if T.degree(n) == 1:
                    T.remove_node(n)
                    removable.remove(n)
                    removed = True
        return T
