# steinernet/wilcoxon_analysis.py

"""
Wilcoxon Rank-Sum Analysis for Steiner Tree Methods

This module evaluates different Steiner tree approximation algorithms using the Wilcoxon signed-rank test
based on their performance (e.g., cost of the resulting tree) on a set of graphs.

@references
1. Wilcoxon F. (1945) Individual comparisons by ranking methods. Biometrics Bulletin 1(6):80–83
2. Afshin Sadeghi and Holger Froehlich, "Steiner tree methods for optimal sub-network identification: an empirical study", BMC Bioinformatics 2013 14:144
"""

import pandas as pd
from scipy.stats import wilcoxon
import itertools
import networkx as nx
from .steiner import SteinerNet

def evaluate_methods_on_graph(graph: nx.Graph, terminals: list[int], methods: list[str], repeats: int = 10) -> list[dict]:
    """
    Evaluate each Steiner method on a single graph and return scores.

    Parameters:
    graph (nx.Graph): The input graph.
    terminals (list): Terminal nodes to connect.
    methods (list): SteinerNet method names to apply.
    repeats (int): Number of repetitions for randomized methods.

    Returns:
    list[dict]: One dict per method with method name, score, and graph ID.
    """
    sn = SteinerNet(graph)
    results = []
    for method in methods:
        tree = sn.steinertree(terminals, method=method, repeats=repeats)
        score = tree.size(weight='weight')
        results.append({'method': method, 'score': score})
    return results

def compare_on_graphs(graphs: list[nx.Graph], terminals_fn, methods: list[str], repeats: int = 10) -> pd.DataFrame:
    """
    Run all methods on all graphs and return DataFrame of results.

    Parameters:
    graphs (list): List of networkx graphs.
    terminals_fn (function): Function G -> list[int] returning terminal nodes.
    methods (list): List of SteinerNet methods.
    repeats (int): Number of repetitions for stochastic methods.

    Returns:
    pd.DataFrame: Results with columns: 'graph_id', 'method', 'score'

    Example:
    >>> from steinerpy.wilcoxon_analysis import compare_on_graphs
    >>> results = compare_on_graphs([G1, G2], lambda G: random.sample(G.nodes(), 3), ['SP', 'KB'])
    """
    all_results = []
    for i, G in enumerate(graphs):
        terminals = terminals_fn(G)
        result = evaluate_methods_on_graph(G, terminals, methods, repeats)
        for r in result:
            r['graph_id'] = i
        all_results.extend(result)
    return pd.DataFrame(all_results)

def pairwise_wilcoxon(data: pd.DataFrame, methods: list[str], metric_col: str = 'score') -> pd.DataFrame:
    """
    Perform pairwise Wilcoxon signed-rank test on multiple methods.

    Parameters:
    data (pd.DataFrame): DataFrame with 'method', 'graph_id', and metric column.
    methods (list): Methods to compare.
    metric_col (str): Metric column name (default 'score').

    Returns:
    pd.DataFrame: Symmetric matrix of p-values.

    Example:
    >>> pvals = pairwise_wilcoxon(results, ['SP', 'KB', 'RSP'])
    """
    results = pd.DataFrame(index=methods, columns=methods, dtype='float')

    for m1, m2 in itertools.combinations(methods, 2):
        d1 = data[data['method'] == m1].sort_values('graph_id')[metric_col].values
        d2 = data[data['method'] == m2].sort_values('graph_id')[metric_col].values
        if len(d1) == len(d2):
            stat, p = wilcoxon(d1, d2)
        else:
            p = float('nan')
        results.loc[m1, m2] = p
        results.loc[m2, m1] = p

    for m in methods:
        results.loc[m, m] = 1.0

    return results
