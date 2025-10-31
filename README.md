# SteinerNet

The Steiner Tree Approach refers to a method used in graph theory and network design to find the most efficient way to connect a set of points (nodes), potentially using extra intermediate points (called Steiner points) to minimize the total connection cost.

This the python eqiuivalent to SteinerNet in R. Released 10 years later on date the R version was released.

## Installation   ![PyPl Total Downloads](https://img.shields.io/pepy/dt/steinernet)

To install:

```bash
pip install steinernet
```

You can install the package locally using pip:

```bash
pip install .
```

Or, for development:

```bash
pip install -e .
```

## Requirements
- Python 3.7+
- networkx

## Usage

```python
import networkx as nx
from steinernet import SteinerNet

# Create a sample graph
G = nx.cycle_graph(6)
terminals = [0, 2, 4]

# Initialize SteinerNet
sn = SteinerNet(G)

# Compute a Steiner tree using the random walk method
T = sn.steinertree(terminals,'ASP', repeats=1, optimize=True)

# Visualize the result
import matplotlib.pyplot as plt
nx.draw(T, with_labels=True)
plt.show()
```

## Turorial
Check the Tutorial on [tutorial file](https://github.com/afshinsadeghi/steinernetpy/blob/main/tutorial/steinernet_benchmark_tutorial.ipynb)

## Documentation

- `SteinerNet(graph)`
    - `graph`: networkx.Graph, the input undirected graph (optionally weighted)
    - **Returns**: SteinerNet object
- `SteinerNet.random_walk_tree(terminals, seed=None)`
    - `terminals`: list of node indices to connect
    - `seed`: (optional) random seed for reproducibility
    - **Returns**: networkx.Graph, a random graph
 
- SteinerNet.steinertree(terminals, method, repeats=1, optimize=True)
- `terminals`: list of node indices to connect
  - `method`: one of the methods   `SP`, `RSP`, `SPM`, `ASP`, `EXA` (see their info in the Reference paper below)  
  - - **Returns**: an approximate Steiner tree made by the selected method 

## Reference
Afshin Sadeghi and Holger Froehlich, "Steiner tree methods for optimal sub-network identification: an empirical study", BMC Bioinformatics 2013 14:144, doi:10.1186/1471-2105-14-144

## License
This project is open source under the [Apache 2.0 License](./LICENSE-2.0.txt). You basically can use it in any commercial or research project.

# Citation
To use this package in your work, cite this article as:

```
@article{sadeghi2013steiner,
  title={Steiner tree methods for optimal sub-network identification: an empirical study},
  author={Sadeghi, Afshin and Fr{\"o}hlich, Holger},
  journal={BMC bioinformatics},
  volume={14},
  pages={1--19},
  year={2013},
  publisher={Springer},
  doi = {https://doi.org/10.1186/1471-2105-14-144}
}
```


Link to [R steinerNet repository](https://github.com/afshinsadeghi/SteinerNet).
Link to [Python SteinerNet repository](https://github.com/afshinsadeghi/steinernetpy).

For bug reports contact me at 🔗 [LinkedIn](https://www.linkedin.com/in/afshin-sadeghi)
