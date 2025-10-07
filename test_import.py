import sys
print("Python path:", sys.path)

try:
    from steinernet.random_walk_subgraph import random_walk_tree
    print("Successfully imported random_walk_tree from steinernet.random_walk_subgraph")
except ImportError as e:
    print(f"Error importing random_walk_tree: {e}")

try:
    from steinernet.steiner import SteinerNet
    print("Successfully imported SteinerNet from steinernet.steiner")
except ImportError as e:
    print(f"Error importing SteinerNet: {e}")

try:
    import steinernet
    print("Successfully imported steinernet package")
    print("steinernet.__file__:", steinernet.__file__)
except ImportError as e:
    print(f"Error importing steinernet package: {e}")
