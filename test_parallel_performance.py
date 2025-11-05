#!/usr/bin/env python
"""
Performance comparison between sequential and parallel implementations of the exact Steiner tree algorithm.
"""

import time
import networkx as nx
import random
import matplotlib.pyplot as plt
from steinernet.steiner import SteinerNet

def generate_random_graph(n_nodes=50, edge_probability=0.2, weight_range=(1, 10)):
    """Generate a random graph for testing."""
    G = nx.gnp_random_graph(n_nodes, edge_probability)
    
    # Ensure the graph is connected
    while not nx.is_connected(G):
        G = nx.gnp_random_graph(n_nodes, edge_probability)
    
    # Add random weights to edges
    for u, v in G.edges():
        G[u][v]['weight'] = random.uniform(weight_range[0], weight_range[1])
    
    return G

def run_performance_test(graph_sizes, n_terminals=5, repeats=3):
    """Run performance tests for different graph sizes."""
    sequential_times = []
    parallel_times = []
    
    for size in graph_sizes:
        seq_time_sum = 0
        par_time_sum = 0
        
        for _ in range(repeats):
            # Generate a random graph
            G = generate_random_graph(n_nodes=size)
            
            # Select random terminals
            terminals = random.sample(list(G.nodes()), n_terminals)
            
            # Create SteinerNet instance
            steiner = SteinerNet(G)
            
            # Run sequential version
            start_time = time.time()
            steiner.steinertree(terminals, method='EXA', parallel=False)
            seq_time = time.time() - start_time
            seq_time_sum += seq_time
            
            # Run parallel version
            start_time = time.time()
            steiner.steinertree(terminals, method='EXA', parallel=True)
            par_time = time.time() - start_time
            par_time_sum += par_time
        
        # Calculate average times
        sequential_times.append(seq_time_sum / repeats)
        parallel_times.append(par_time_sum / repeats)
        
        print(f"Graph size: {size}")
        print(f"  Sequential: {seq_time_sum / repeats:.4f} seconds")
        print(f"  Parallel:   {par_time_sum / repeats:.4f} seconds")
        print(f"  Speedup:    {(seq_time_sum / par_time_sum):.2f}x")
    
    return sequential_times, parallel_times

def plot_results(graph_sizes, sequential_times, parallel_times):
    """Plot the performance comparison results."""
    plt.figure(figsize=(10, 6))
    
    plt.plot(graph_sizes, sequential_times, 'o-', label='Sequential')
    plt.plot(graph_sizes, parallel_times, 's-', label='Parallel')
    
    plt.xlabel('Graph Size (Number of Nodes)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Comparison: Sequential vs. Parallel')
    plt.legend()
    plt.grid(True)
    
    # Calculate speedup
    speedups = [seq / par for seq, par in zip(sequential_times, parallel_times)]
    
    # Add speedup as text annotations
    for i, size in enumerate(graph_sizes):
        plt.annotate(f"{speedups[i]:.2f}x", 
                     xy=(size, parallel_times[i]),
                     xytext=(5, 10), 
                     textcoords='offset points')
    
    plt.savefig('performance_comparison.png')
    plt.close()

if __name__ == "__main__":
    # Define graph sizes to test
    # Start with small sizes for quick testing, adjust as needed
    graph_sizes = [15, 20, 25]
    
    # Run the performance test
    sequential_times, parallel_times = run_performance_test(graph_sizes)
    
    # Plot the results
    plot_results(graph_sizes, sequential_times, parallel_times)
    
    print("\nPerformance test completed. Results saved to 'performance_comparison.png'")
