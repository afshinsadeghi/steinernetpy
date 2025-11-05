#!/usr/bin/env python
"""
Example demonstrating how to use the parallelized Steiner tree algorithms.
"""

import networkx as nx
import matplotlib.pyplot as plt
import time
from steinernet.steiner import SteinerNet

def create_example_graph():
    """Create a simple example graph for demonstration."""
    G = nx.Graph()
    
    # Add nodes
    for i in range(10):
        G.add_node(i)
    
    # Add edges with weights
    edges = [
        (0, 1, 1.0), (0, 2, 2.0), (1, 2, 1.5), (1, 3, 2.0),
        (2, 3, 1.0), (2, 4, 2.5), (3, 4, 1.0), (3, 5, 3.0),
        (4, 5, 1.0), (4, 6, 2.0), (5, 6, 1.5), (5, 7, 2.0),
        (6, 7, 1.0), (6, 8, 2.5), (7, 8, 1.0), (7, 9, 3.0),
        (8, 9, 1.0)
    ]
    
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    
    return G

def draw_graph(G, tree=None, terminals=None, title="Graph"):
    """Draw the graph and highlight the Steiner tree if provided."""
    plt.figure(figsize=(10, 6))
    
    # Position nodes using spring layout
    pos = nx.spring_layout(G, seed=42)
    
    # Draw the original graph
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos)
    
    # Draw edge weights
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Highlight the Steiner tree if provided
    if tree is not None:
        nx.draw_networkx_edges(tree, pos, width=3.0, edge_color='red')
    
    # Highlight terminal nodes if provided
    if terminals is not None:
        nx.draw_networkx_nodes(G, pos, nodelist=terminals, node_color='red', node_size=500)
    
    plt.title(title)
    plt.axis('off')
    return plt

def main():
    # Create an example graph
    G = create_example_graph()
    
    # Define terminal nodes
    terminals = [0, 5, 9]
    
    # Create a SteinerNet instance
    steiner = SteinerNet(G)
    
    # Draw the original graph with terminals highlighted
    plt = draw_graph(G, terminals=terminals, title="Original Graph with Terminal Nodes")
    plt.savefig("example_original_graph.png")
    plt.close()
    
    print("Finding Steiner tree using sequential algorithm...")
    start_time = time.time()
    sequential_tree = steiner.steinertree(terminals, method='EXA', parallel=False)
    sequential_time = time.time() - start_time
    sequential_cost = sequential_tree.size(weight='weight')
    
    print(f"Sequential algorithm completed in {sequential_time:.4f} seconds")
    print(f"Sequential tree cost: {sequential_cost:.2f}")
    
    # Draw the sequential result
    plt = draw_graph(G, tree=sequential_tree, terminals=terminals, 
                    title=f"Sequential Steiner Tree (Cost: {sequential_cost:.2f})")
    plt.savefig("example_sequential_tree.png")
    plt.close()
    
    print("\nFinding Steiner tree using parallel algorithm...")
    start_time = time.time()
    parallel_tree = steiner.steinertree(terminals, method='EXA', parallel=True)
    parallel_time = time.time() - start_time
    parallel_cost = parallel_tree.size(weight='weight')
    
    print(f"Parallel algorithm completed in {parallel_time:.4f} seconds")
    print(f"Parallel tree cost: {parallel_cost:.2f}")
    
    # Draw the parallel result
    plt = draw_graph(G, tree=parallel_tree, terminals=terminals, 
                    title=f"Parallel Steiner Tree (Cost: {parallel_cost:.2f})")
    plt.savefig("example_parallel_tree.png")
    plt.close()
    
    # Compare the results
    print("\nComparison:")
    print(f"Sequential time: {sequential_time:.4f} seconds")
    print(f"Parallel time:   {parallel_time:.4f} seconds")
    print(f"Speedup:         {sequential_time / parallel_time:.2f}x")
    print(f"Both algorithms found trees with the same cost: {sequential_cost == parallel_cost}")
    
    # Try with a specific number of processes
    print("\nFinding Steiner tree using parallel algorithm with 2 processes...")
    start_time = time.time()
    parallel_tree_2 = steiner.steinertree(terminals, method='EXA', parallel=True, n_processes=2)
    parallel_time_2 = time.time() - start_time
    
    print(f"Parallel algorithm (2 processes) completed in {parallel_time_2:.4f} seconds")
    print(f"Speedup compared to sequential: {sequential_time / parallel_time_2:.2f}x")

if __name__ == "__main__":
    main()

# Test on M2 pro machine:

# Graph size: 15
#  Sequential: 0.0572 seconds
#  Parallel:   2.0993 seconds
#  Speedup:    0.03x
#Graph size: 20
#  Sequential: 2.1141 seconds
#  Parallel:   2.5754 seconds
#  Speedup:    0.82x
#Graph size: 25
#  Sequential: 86.4288 seconds
#  Parallel:   28.5924 seconds
#  Speedup:    3.02x